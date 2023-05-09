# SPDX-License-Identifier: BSD-3-Clause
import json
import logging as log

from datetime  import datetime
from enum      import IntEnum, unique
from hashlib   import blake2b
from io        import BytesIO
from typing    import BinaryIO, Union

import msgpack

from arrow     import Arrow
from construct import (
	Bytes, Checksum, ChecksumError, Compressed, Computed,
	Const, ConstError, Default, Enum, GreedyBytes, Hex,
	Int8ul, Int32ub, Int32ul, Int64ul, Prefixed, Rebuild,
	Struct, Switch, Tunnel, this
)

__all__ = (
	'XCMFile',
	'Compression',
	'Content',
)

EPOCH = Arrow(1970, 1, 1)

def _timestamp_from_raw(this) -> Arrow:
	ts = (this.raw.high << 32) + this.raw.low
	return EPOCH.shift(seconds = ts * 1e-6)

def _timestamp_to_raw(this):
	ts = this.value
	if not isinstance(ts, Arrow):
		ts = Arrow.fromdatetime(ts)

	val = int((ts - EPOCH).total_seconds() * 1e6)
	return { 'low': val & 0xFFFFFFFF, 'high': val >> 32 }


class CompressedZSTD(Tunnel):

	def __init__(self, subcon, level: int = 19):
		super().__init__(subcon)
		import zstandard

		self.lib = zstandard
		self.level = level

	def _decode(self, data, context, path):
		return self.lib.decompress(data)

	def _encode(self, data, context, path):
		return self.lib.compress(data, level = self.level)


@unique
class Compression(IntEnum):
	ZSTD = 0x01
	LZMA = 0x02
	ZLIB = 0x03
	BZ2  = 0x04
	GZIP = 0x05
	NONE = 0xFF

	def __str__(self):
		return {
			Compression.ZSTD: 'ZSTD',
			Compression.LZMA: 'LZMA',
			Compression.ZLIB: 'ZLIB',
			Compression.BZ2: 'BZ2',
			Compression.GZIP: 'GZIP',
			Compression.NONE: 'NONE',
		}.get(self)

class Content(IntEnum):
	MSGPACK = 0x00
	JSON    = 0x01
	BLOB    = 0x02

	def __str__(self):
		return {
			Content.MSGPACK: 'MSGPACK',
			Content.JSON: 'JSON',
			Content.BLOB: 'BLOB',
		}.get(self)


xcm = 'XCM' / Struct(
	'header' / Struct(
		# `XCM1`
		'magic'       / Hex(Const(0x58434D31, Int32ub)),
		'timestamp'   / Default(Struct(
			'raw' / Rebuild(Struct(
				'high' / Hex(Int32ul),
				'low'  / Hex(Int32ul),
			), _timestamp_to_raw),
			'value' / Computed(_timestamp_from_raw)
		), { 'value': datetime.utcnow()}),
		'compression' / Hex(Default(Enum(Int8ul, Compression), Compression.ZSTD)),
		'format'      / Hex(Default(Enum(Int8ul, Content),     Content.MSGPACK)),
	),
	# 'data'   / Prefixed(Int64ul, Switch(
	# 	this.header.compression, {
	# 		Compression.ZSTD: CompressedZSTD(GreedyBytes),
	# 		Compression.LZMA: Compressed(GreedyBytes, 'lzma'),
	# 		Compression.ZLIB: Compressed(GreedyBytes, 'zlib'),
	# 		Compression.BZ2 : Compressed(GreedyBytes, 'bzip2'),
	# 		Compression.GZIP: Compressed(GreedyBytes, 'gzip'),
	# 		Compression.NONE: GreedyBytes,
	# 	}
	# )),
	'data'   / Prefixed(Int64ul, CompressedZSTD(GreedyBytes)),
	'checksum' / Checksum(
		Bytes(8),
		lambda data: blake2b(data, digest_size = 8).digest(),
		this.data
	)
)


class XCMFile:

	def __init__(self):
		pass

	@staticmethod
	def dump(
		target: Union[BinaryIO, BytesIO], data: bytes, contents: Content = Content.BLOB
	):

		xcm.build_stream({
			'header': {
				'format': contents,
			},
			'data': data
		}, target)


	@staticmethod
	def load(data: Union[bytes, BinaryIO, BytesIO]) -> 'XCMFile':
		if isinstance(data, bytes):
			_data = BytesIO(data)
		else:
			_data = data

		file = XCMFile()
		try:
			file._xcm_file = xcm.parse_stream(_data)
		except ConstError:
			raise RuntimeError('Incorrect Magic Number, not a valid XCM?')
		except ChecksumError:
			raise RuntimeError('Checksum mismatch, corrupted XCM?')
		log.debug('XCM File:')
		log.debug(file._xcm_file)
		return file

	@property
	def size(self) -> int:
		return len(self._xcm_file.data)

	@property
	def raw_data(self):
		return self._xcm_file.data

	@property
	def deserialize(self):
		if self.content == Content.MSGPACK:
			return msgpack.loads(self.raw_data)
		elif self.content == Content.JSON:
			return json.loads(self.raw_data)
		elif self.content == Content.BLOB:
			return self.data

	@property
	def timestamp(self) -> Arrow:
		return self._xcm_file.header.timestamp.value

	@property
	def compression(self) -> Compression:
		return Compression(int(self._xcm_file.header.compression))

	@property
	def content(self) -> Content:
		return Content(int(self._xcm_file.header.format))

	def __str__(self) -> str:
		return f'<XCMFile X: {self.compression} C: {self.content} S: {self.size} TS: \'{self.timestamp}\'>'

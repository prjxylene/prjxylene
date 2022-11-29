# SPDX-License-Identifier: BSD-3-Clause
import logging        as log
from datetime         import datetime
import subprocess
from typing           import List, Tuple
from pathlib          import Path

from prjxylene.common import (
	XYLENE_WORKING_DIR
)

__all__ = (
	'Vivado'
)

class Vivado:
	VIVADO_WORKING_DIR = (XYLENE_WORKING_DIR / 'vivado')

	@staticmethod
	def spawn_tcl(
		_log : bool, journal : bool, tcl_file : Path, tcl_args : List[str]
	) -> bool:
		success = False
		with Vivado(log = _log, journal = journal) as v:
			success = v.run_tcl(
				tcl_file = str(tcl_file.resolve()),
				tcl_args = tcl_args
			)


			if not success:
				log.info('Writing Vivado output logs')
				with open((XYLENE_WORKING_DIR / f'{tcl_file.name}.stdout'), 'w+') as stdout:
					stdout.write(v.stdout.decode('utf-8'))

				with open((XYLENE_WORKING_DIR / f'{tcl_file.name}.stderr'), 'w+') as stderr:
					stderr.write(v.stderr.decode('utf-8'))

		return success

	def __init__(self, *, log : bool = True,
				journal : bool = True, cwd : str = None,
				extra_args : list = () , cleanup : bool = True) -> None:

		if not self.VIVADO_WORKING_DIR.exists():
			self.VIVADO_WORKING_DIR.mkdir()

		self.run_dir = (self.VIVADO_WORKING_DIR / str(datetime.now().timestamp()))
		self.cleanup = cleanup
		self.stdout = None
		self.stderr = None

		self.vivado_args  = [
			'vivado',
			'-tempDir',
			str(self.run_dir),
			*extra_args
		]

		self.log = log
		if not log:
			self.vivado_args.append('-nolog')


		self.journal = journal
		if not journal:
			self.vivado_args.append('-nojournal')

		self.cwd = cwd if cwd is not None else self.VIVADO_WORKING_DIR

	def __enter__(self):
		return self

	def __exit__(self, t, v, tb):
		from shutil import rmtree
		if self.cleanup and self.run_dir.exists():
			rmtree(self.run_dir)

		if not (t is None and v is None and tb is None):
			return


	def run(self, *, args : list, silent = True) -> bool:

		log_args = []
		if self.log:
			log_args += ('-log', f'vivado.{datetime.now().timestamp()}.log')

		if self.journal:
			log_args += ('-journal', f'vivado.{datetime.now().timestamp()}.jou')


		run_list = [
			*self.vivado_args,
			*log_args,
			*args,
		]

		log.debug(f'Running \'{" ".join(run_list)}\'')

		if not silent:
			ret = subprocess.run(
				run_list,
				capture_output = True,
				cwd = str(self.cwd)
			)
		else:
			ret = subprocess.run(
				run_list,
				capture_output = True,
				cwd = str(self.cwd)
			)

		self.stdout = ret.stdout
		self.stderr = ret.stderr

		if ret.returncode != 0:
			return False

		return True

	def run_tcl(self, *, tcl_file, tcl_args, silent = True) -> bool:
		if not silent:
			log.info(f'Running TCL file: \'{tcl_file}\'')
			log.info(f'TCL Script args: {tcl_args}')

		return self.run(args = [
			'-mode', 'batch',
			'-source', tcl_file,
			'-tclargs', *tcl_args
		], silent = silent)

# SPDX-License-Identifier: BSD-3-Clause
from cProfile import run
import logging     as log
from pathlib       import Path
from os            import getenv
from datetime      import datetime
import subprocess


from xylene_common import (
	XYLENE_WORKING_DIR
)

__all__ = (
	'Vivado'
)

class Vivado:
	VIVADO_WORKING_DIR = (XYLENE_WORKING_DIR / 'vivado')
	def __init__(self, *, log : bool = True, journal : bool = True, cwd : str = None, extra_args : list = ()) -> None:
		if not self.VIVADO_WORKING_DIR.exists():
			self.VIVADO_WORKING_DIR.mkdir()

		self.run_dir = (self.VIVADO_WORKING_DIR / str(datetime.now().timestamp()))

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

	def run(self, *, args : list) -> bool:

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

		subprocess.run(
			run_list,
			stderr = subprocess.DEVNULL,
			stdout = subprocess.DEVNULL,
			cwd = str(self.cwd)
		)

	def run_tcl(self, *, tcl_file, tcl_args):
		log.info(f'Running TCL file: \'{tcl_file}\'')
		log.info(f'TCL Script args: {tcl_args}')
		self.run(args = [
			'-mode', 'batch',
			'-source', tcl_file,
			'-tclargs', *tcl_args
		])

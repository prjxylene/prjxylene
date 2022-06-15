# SPDX-License-Identifier: BSD-3-Clause
import logging       as log
from pathlib         import Path
from os              import getenv
from datetime        import datetime
import subprocess


from xylene.common import (
	XYLENE_WORKING_DIR
)

__all__ = (
	'Vivado'
)

class Vivado:
	VIVADO_WORKING_DIR = (XYLENE_WORKING_DIR / 'vivado')
	def __init__(self, *, log : bool = True, journal : bool = True, cwd : str = None, extra_args : list = () , cleanup : bool = True) -> None:
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

# SPDX-License-Identifier: BSD-3-Clause
import logging    as log
from argparse     import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib      import Path
from os           import getenv

from rich         import traceback
from rich.logging import RichHandler

__all__ = (
	'general_init',
	'init_cli',
	'setup_logging',

	'XYLENE_ENV',
	'XYLENE_WORKING_DIR',
	'XILINX_VIVADO',

	'XYLENE_SCRIPTS',
	'XYLENE_DB_DIR',
	'XYLENE_PART_INDEX_DIR'
)

XYLENE_ENV         = Path(getenv('XYLENE_ENV'))
XYLENE_WORKING_DIR = Path(getenv('XYLENE_WORKING_DIR'))
XILINX_VIVADO      = Path(getenv('XILINX_VIVADO'))


XYLENE_SCRIPTS        = (XYLENE_ENV / 'etc/scripts')
XYLENE_DB_DIR         = (XYLENE_ENV / 'db')
XYLENE_PART_INDEX_DIR = (XYLENE_DB_DIR / 'part_indices')

def setup_logging(verbose = False) -> None:
	'''Initialize logging subscriber

	Set up the built-in rich based logging subscriber, and force it
	to be the one at runtime in case there is already one set up.

	Parameters
	----------
	verbose : bool
		Verbose output

	'''

	log.basicConfig(
		force    = True,
		format   = '%(message)s',
		datefmt  = '[%X]',
		level    = log.DEBUG if verbose else log.INFO,
		handlers = [
			RichHandler(rich_tracebacks = True)
		]
	)


def general_init():
	traceback.install()
	setup_logging()

def init_cli(prog, desc = ''):
	parser = ArgumentParser(
		formatter_class = ArgumentDefaultsHelpFormatter,
		description     = desc,
		prog            = prog,
	)



	return parser

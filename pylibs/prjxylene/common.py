# SPDX-License-Identifier: BSD-3-Clause
import logging    as log
from argparse     import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib      import Path
from os           import getenv

from rich         import traceback
from rich.logging import RichHandler

__all__ = (
	'main',

	'XYLENE_ENV',
	'XYLENE_WORKING_DIR',
	'XILINX_VIVADO',

	'XYELNE_CACHE_DIR',

	'XYLENE_SCRIPTS',
	'XYLENE_DB_DIR',
)

XYLENE_ENV         = Path(getenv('XYLENE_ENV'))
XYLENE_WORKING_DIR = Path(getenv('XYLENE_WORKING_DIR'))
XILINX_VIVADO      = Path(getenv('XILINX_VIVADO'))

XYELNE_CACHE_DIR   = (XYLENE_WORKING_DIR / 'cache')

XYLENE_SCRIPTS         = (XYLENE_ENV    / 'etc/scripts')
XYLENE_DB_DIR          = (XYLENE_ENV    / 'db')


def main(tool_main, tool_name, tool_desc, parser_init = None):
	traceback.install()

	parser = ArgumentParser(
		formatter_class = ArgumentDefaultsHelpFormatter,
		description     = tool_desc,
		prog            = tool_name,
	)

	core_options = parser.add_argument_group('Core Xylene Options')
	core_options.add_argument(
		'--verbose', '-V',
		action = 'store_true',
		help   = 'Enable verbose logging'
	)

	if parser_init is not None:
		tool_parser = parser.add_argument_group(f'{tool_name} Options')
		parser_init(tool_parser)

	args = parser.parse_args()

	log.basicConfig(
		force    = True,
		format   = '%(message)s',
		datefmt  = '[%X]',
		level    = log.DEBUG if args.verbose else log.INFO,
		handlers = [
			RichHandler(rich_tracebacks = True)
		]
	)

	return tool_main(args)

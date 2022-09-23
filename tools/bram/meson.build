# SPDX-License-Identifier: BSD-3-Clause
xy_bram_srcs = files([
	'main.cc'
])
xy_bram_inc  = include_directories('./include')

xy_bram = executable(
	'xy-bram',
	xy_bram_srcs,
	include_directories: [
		root_inc,
		xy_bram_inc,
	],
	gnu_symbol_visibility: 'inlineshidden',

	implicit_include_directories: false,

	dependencies: [
		substrate,
	],
	link_with: [
		libxylene_core,
		libxylene_common,
		libxylene_database,
	],
	install: true
)

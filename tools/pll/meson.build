# SPDX-License-Identifier: BSD-3-Clause
xy_pll_srcs = files([
	'main.cc'
])
xy_pll_inc  = include_directories('./include')

xy_pll = executable(
	'xy-pll',
	xy_pll_srcs,
	include_directories: [
		root_inc,
		xy_pll_inc,
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

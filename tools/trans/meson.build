# SPDX-License-Identifier: BSD-3-Clause
xy_trans_srcs = files([
	'main.cc'
])
xy_trans_inc  = include_directories('./include')

xy_trans = executable(
	'xy-trans',
	xy_trans_srcs,
	include_directories: [
		root_inc,
		xy_trans_inc,
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

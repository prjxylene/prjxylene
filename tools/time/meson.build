# SPDX-License-Identifier: BSD-3-Clause
xy_time_srcs = files([
	'main.cc'
])
xy_time_inc  = include_directories('./include')

xy_trans = executable(
	'xy-time',
	xy_time_srcs,
	include_directories: [
		root_inc,
		xy_time_inc,
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

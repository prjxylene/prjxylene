# SPDX-License-Identifier: BSD-3-Clause
xy_bit_srcs = files([
	'main.cc'
])
xy_bit_inc  = include_directories('./include')

xy_bit = executable(
	'xy-bit',
	xy_bit_srcs,
	include_directories: [
		root_inc,
		xy_bit_inc,
	],
	gnu_symbol_visibility: 'inlineshidden',

	implicit_include_directories: false,

	dependencies: [
		substrate,
	],
	link_with: [
		libxylene_core,
		libxylene_common,
		libxylene_bitstream,
	],
	install: true
)

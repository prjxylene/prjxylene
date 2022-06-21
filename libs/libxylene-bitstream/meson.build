# SPDX-License-Identifier: BSD-3-Clause

libxylene_bitstream_inc = include_directories('.')

libxylene_bitstream_srcs = files([

])

libxylene_bitstream_hdrs = files([

])

libxylene_bitstream = library(
	'xylene-bitstream',
	libxylene_bitstream_srcs,

	include_directories: [
		root_inc,
		libxylene_bitstream_inc
	],
	gnu_symbol_visibility: 'inlineshidden',

	implicit_include_directories: false,
	pic: true,
	cpp_args: [
		'-DXYLENE_BUILD_INTERNAL'
	],

	dependencies: [
		substrate,
		libxylene_common_dep,
	],

	install: true
)

install_headers(
	libxylene_bitstream_hdrs,
	subdir: 'xylene/libxylene-bistream'
)

libxylene_bitstream_dep = declare_dependency(
	include_directories: libxylene_bitstream_inc,
	link_with: libxylene_bitstream,
	version: meson.project_version()
)

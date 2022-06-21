# SPDX-License-Identifier: BSD-3-Clause

libxylene_core_inc = include_directories('.')

libxylene_core_srcs = files([

])

libxylene_core_hdrs = files([

])

libxylene_core = library(
	'xylene-bitstream',
	libxylene_core_srcs,

	include_directories: [
		root_inc,
		libxylene_core_inc
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
		libxylene_bitstream_dep,
		libxylene_database_dep
	],

	install: true
)

install_headers(
	libxylene_core_hdrs,
	subdir: 'xylene/libxylene'
)

libxylene_core_dep = declare_dependency(
	include_directories: libxylene_core_inc,
	link_with: libxylene_core,
	version: meson.project_version()
)

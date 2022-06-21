# SPDX-License-Identifier: BSD-3-Clause

libxylene_database_inc = include_directories('.')

libxylene_database_srcs = files([

])

libxylene_database_hdrs = files([

])

libxylene_database = library(
	'xylene-database',
	libxylene_database_srcs,

	include_directories: [
		root_inc,
		libxylene_database_inc
	],
	gnu_symbol_visibility: 'inlineshidden',

	implicit_include_directories: false,
	pic: true,
	cpp_args: [
		'-DXYLENE_BUILD_INTERNAL'
	],

	dependencies: [
		substrate,
		zstd,
		zlib,
		libxylene_common_dep,
	],

	install: true
)

install_headers(
	libxylene_database_hdrs,
	subdir: 'xylene/libxylene-database'
)

libxylene_database_dep = declare_dependency(
	include_directories: libxylene_database_inc,
	link_with: libxylene_database,
	version: meson.project_version()
)

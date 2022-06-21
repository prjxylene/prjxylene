# SPDX-License-Identifier: BSD-3-Clause

libxylene_common_inc = include_directories('.')

libxylene_common_srcs = files([

])

libxylene_common_hdrs = files([
	'utility.hh'
])

libxylene_common = library(
	'xylene-common',
	libxylene_common_srcs,

	include_directories: [
		root_inc,
		libxylene_common_inc
	],
	gnu_symbol_visibility: 'inlineshidden',

	implicit_include_directories: false,
	pic: true,
	cpp_args: [
		'-DXYLENE_BUILD_INTERNAL'
	],

	dependencies: [
		substrate,
	],

	install: true
)

install_headers(
	libxylene_common_srcs,
	subdir: 'xylene/libxylene-common'
)

libxylene_common_dep = declare_dependency(
	include_directories: libxylene_common_inc,
	link_with: libxylene_common,
	version: meson.project_version()
)

# SPDX-License-Identifier: BSD-3-Clause

if get_option('binding_install_dir') == ''
	binding_install_dir = py.get_install_dir()
else
	binding_install_dir = get_option('binding_install_dir')
endif

message('Installing python bindings to @0@'.format(binding_install_dir))

libxylene_python =  py.extension_module(
	'xylene',
	files([
		'xylene.cc'
	]),

	include_directories: [
		root_inc,
	],

	dependencies: [
		libxylene_bitstream_dep,
		libxylene_core_dep,
		libxylene_common_dep,
		libxylene_database_dep,
		pybind11
	],

	cpp_args: [
		'-DXYLENE_BUILD_BINDINGS'
	],

	install: true,
	install_dir: binding_install_dir
)

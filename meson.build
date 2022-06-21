# SPDX-License-Identifier: BSD-3-Clause
project(
	'prjxylene',
	'cpp',
	default_options: [
		'cpp_std=c++20',
		'warning_level=3',
		'build.cpp_std=c++20',
		'buildtype=debugoptimized',
		'strip=true',
		'b_ndebug=if-release',
		'b_lto=true'
	],
	version: '0.0.1',
	license: [
		'BSD-3-Clause',
	],
	meson_version: '>=0.57.0',
)

cxx = meson.get_compiler('cpp')

if get_option('cpp_std') not in ['c++17', 'c++20', 'c++23', 'gnu++17', 'gnu++20', 'gnu++23']
	error('Unsupported C++ Version @0@, must be c++17/gnu++17 or newer'.format(get_option('cpp_std')))
endif

extended_warnings = [
	'-Wdouble-promotion',
	'-Wformat=2',
	'-Wformat-overflow=2',
	'-Wformat-signedness',
	'-Wformat-truncation',
	'-Wnull-dereference',
	'-Wmissing-attributes',
	'-Wmissing-braces',
	'-Wsequence-point',
	'-Wreturn-type',
	'-Wunused',
	'-Wunused-local-typedefs',
	'-Wunused-const-variable=2',
	'-Wmaybe-uninitialized',
	'-Wunknown-pragmas',
	'-Wstrict-aliasing',
	'-Wstrict-overflow=3',
	'-Wstring-compare',
	'-Wstringop-overflow',
	'-Warith-conversion',
	'-Wvla-parameter',
	'-Wduplicated-branches',
	'-Wshadow=local',
	'-Wunsafe-loop-optimizations',
	'-Wbad-function-cast',
	'-Wcast-qual',
	'-Wcast-align=strict',
	'-Wcast-function-type',
	'-Wconversion',
	'-Wdangling-else',
	'-Wsign-conversion',
	'-Wfloat-conversion',
	'-Wpacked',
	'-Wpadded',
	'-Wredundant-decls',
	'-Winline',
	'-Wvla',
	'-Wstack-protector',
	'-Wunsuffixed-float-constant',
	'-Wimplicit-fallthrough',
]

add_project_arguments(
	cxx.get_supported_arguments(extended_warnings),
	language: 'cpp'
)

py = import('python')
py = py.find_installation(
	'python3',
	required: false,
	modules: []
)

global_deps = [
	dependency('threads', required: true),
]

zstd     = dependency('zstd',     required: false, modules: ['zstd::libzstd_shared'], version: '>=1.4.5' )
zlib     = dependency('zlib',     required: false, version: '>=1.2.12')
pybind11 = dependency('pybind11', required: false, version: '>=2.7.0' )

if not zstd.found()
	message('Did not find local zstd install, bundling')
	zstd_wrap = subproject('zstd', default_options: [])
	zstd = zstd_wrap.get_variable('zstd_dep')
endif

if not zlib.found()
	message('Did not find local zlib install, bundling')
	zlib_wrap = subproject('zlib', default_options: [])
	zlib = zlib_wrap.get_variable('zlib_dep')
endif

if not pybind11.found()
	message('Did not find local pybind11 install, bundling')
	pybind11_wrap = subproject('pybind11', default_options: [])
	pybind11 = pybind11_wrap.get_variable('pybind11_dep')
endif

subdir('libs')
subdir('bindings')
# subdir('utilities')
subdir('tools')

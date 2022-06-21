// SPDX-License-Identifier: BSD-3-Clause

#include <pybind11/pybind11.h>

#include <xylene_config.hh>

namespace py = pybind11;

PYBIND11_MODULE(xylene, m) {

	m.doc() = "Xilinx® FPGA documentation project";
	m.attr("__version__") = Xylene::Config::version;

	[[maybe_unused]]
	auto bitstream = m.def_submodule("bitstream", "Xylene bitstream management and interfaces");
	[[maybe_unused]]
	auto core      = m.def_submodule("core",      "Core Xylene"                               );
	[[maybe_unused]]
	auto common    = m.def_submodule("common",    "Common support utilities for Xylene"       );
	[[maybe_unused]]
	auto database  = m.def_submodule("database",  "Xylene database management and interfaces" );
	[[maybe_unused]]
	auto tools     = m.def_submodule("tools",     "Various utilities and tools for Xylene"    );

}

/* SPDX-License-Identifier: BSD-3-Clause */
#include <xylene_config.hh>

#include <array>
#include <string_view>
#include <cstdint>
#include <getopt.h>
#include <unistd.h>

#include <substrate/utility>
#include <substrate/console>
#include <substrate/conversions>

using namespace std::literals::string_view_literals;

namespace xyc = Xylene::Config;

static const std::array<option, 5> options{{
	{ "help",      no_argument, 0, 'h' },
	{ "version",   no_argument, 0, 'v' },
	{ "debug",     no_argument, 0, 'd' },
	{ "no-banner", no_argument, 0, 'b' },

	{ 0,           0,           0,  0  },
}};

void print_banner();
void print_help();
void print_version();

int main(int argc, char** argv) {
	substrate::console = {stdout, stderr};
	substrate::console.showDebug(false);

	bool show_banner{true};

	int32_t opt{};
	int32_t opt_idx{0};
	while ((opt = getopt_long(argc, argv, "hvdb", options.data(), &opt_idx))) {
		switch (opt) {
			case 'h': {
				print_help();
				exit(1);
			} case 'v': {
				print_version();
				exit(0);
			} case 'd': {
				substrate::console.showDebug(true);
				break;
			} case 'b': {
				show_banner = false;
				break;
			} case '?': {
			} default: {
				exit(1);
			}
		}
	}

	if (show_banner)
		print_banner();

	return 0;
}

void print_banner() {
	substrate::console.writeln(
		"xy-pll v"sv, xyc::version,
		" ("sv, xyc::compiler_name,
		" "sv, xyc::compiler_version,
		" "sv, xyc::build_system,
		"-"sv, xyc::build_arch,
		")"sv
	);
	substrate::console.writeln("\nxy-bit: Xilinx FPGA® PLL utility\n"sv);

	substrate::console.writeln("xy-pll is part of the Xylene project <https://github.com/prjxylene>"sv);
	substrate::console.writeln("xy-pll is licensed under the BSD-3-Clause <https://spdx.org/licenses/BSD-3-Clause.html>"sv);
	substrate::console.writeln("\nPlease report bugs at <"sv, xyc::bugreport_url, ">"sv);
}

void print_help() {
	print_banner();

	substrate::console.writeln("\nUsage:"sv);
	substrate::console.writeln("\nxy-pll[options]\n"sv);
	substrate::console.writeln("  --help,      -h       Print this help text and exit"sv);
	substrate::console.writeln("  --version,   -v       Print version and exit"sv);
	substrate::console.writeln("  --debug,     -d       Prints debug output THIS WILL GENERATE A LOT OF MESSAGES"sv);
	substrate::console.writeln("  --no-banner, -n       Do not print the banner"sv);

}


void print_version() {
	substrate::console.writeln("xy-pll v"sv, xyc::version);
}

# Project Xylene - Xilinx® FPGA Documentation

Xylene is a project to document as much as possible about as many as possible of the Xilinx®
FPGA families.

This project contains tools and libraries that assist in the documentation and transforming the documentation into something useable for routing.

We maintain a [nextpnr](https://github.com/prjxylene/nextpnr) and [yosys](https://github.com/prjxylene/yosys) fork for experimentation with the hopes of eventually upstreaming the changes
to allow for a fully Open-Source FPGA flow for Xilinx® FPGAs

## Documentation

Documentation about the project, tools, and database can be found at [prjxylene.fpga.moe](https://prjxylene.fpga.moe/).

## Getting Started

**NOTE:** Only Linux is supported for developing on PrjXylene at this time.

### Prerequisites

Before you can build and use PrjXylene, you need to install the following software:
 * git
 * python >= 3.9
 * gcc/g++ >= 11
 * meson >= 0.60.0
 * graphviz >= 4.0.0

To build Yosys and nextpnr, also install their build and runtime dependencies:
 * clang
 * bison
 * flex
 * libreadline
 * gawk
 * tcl
 * libffi
 * graphviz
 * xdot
 * qt5
 * libboost-all
 * cmake
 * libeigen4

If you plan to do any documentation or fuzzing, you also need [Vivado 2022.1](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/2022-1.html)

### Clone the Repo

Next, just clone the main PrjXylene repository:
```
git clone https://github.com/prjxylene/prjxylene
```

### Environment Setup

To set up the PrjXylene environment, source the `env.sh` script in the
root of the repository, that will take care of most of the setup needed
automatically

## License

Project Xylene falls under two licenses:

The software and database is licensed under the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) and can be found in the [LICENSE](LICENSE) file.

The documentation is licensed under the Creative Commons [CC-BY-SA](https://creativecommons.org/licenses/by-sa/2.0/) and can be found in the [docs/LICENSE](docs/LICENSE) file.

## Legalities

Xilinx®, Artix®, Kintex®, Spartan®, Versal®, Virtex®, and Zynq® are registered trademarks of Xilinx, Inc, and Advanced Micro Devices Inc.

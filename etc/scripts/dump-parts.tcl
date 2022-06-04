# SPDX-License-Identifier: BSD-3-Clause
# This TCL scripts dumps the internal Vivado
# parts cache into a JSON file
# run with `vivado -mode batch -source $XYLENE_ENV/etc/scripts/dump-parts.tcl -tclargs $XYLENE_WORKING_DIR/raw-parts.json

proc dump_parts { fname } {
	set file [open $fname "w+"]

	set vivado_version [version -short]

	puts $file "{"
	puts $file "	\"vivado_version\": \"$vivado_version\", "
	puts $file "	\"parts\": \["

	set parts [get_parts]

	foreach prt $parts {
		set props [list_property $prt]
		puts $file "		{"
		foreach prop $props {
			set p_val [get_property $prop $prt]
			puts $file "			\"$prop\": \"$p_val\","
		}
		puts $file "		},"
	}

	puts $file "	\]"
	puts $file "}"
}

if { $argc == 1 } {
	set fname [lindex $argv 0]
	dump_parts $fname
} {
	error "Specify a file name"
	exit
}
exit

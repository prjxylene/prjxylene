# SPDX-License-Identifier: BSD-3-Clause
import re
import textwrap
from datetime import datetime

from jinja2   import Environment

__all__ = (
	'render_template',
)

TEMPLATES = {
	'dump_part_list': r'''
		# {{spdx_license}}
		{{autogenerated}}

		{% raw %}proc dump_parts { fname } {{% endraw %}

			set file [open $fname "w+"]
			set vivado_version [version -short]

			puts $file "{% raw %}{{% endraw %}"
			puts $file "\t\"vivado_version\": \"$vivado_version\", "
			puts $file "\t\"parts\": \["

			set parts [get_parts]

			{% raw %}
			foreach part $parts {
			{% endraw %}
				puts $file "\t\t\"$part\","
			{% raw %}
			}
			{% endraw %}
			# HACK: Ensure that the last entry is empty to terminate the list
			puts $file "\t\t\"\""
			puts $file "\t\]"
			puts $file "{% raw %}}{% endraw %}"

		{% raw %}}{% endraw %}

		{% raw %}if { $argc == 1 } {
		{% endraw %}
			set fname [lindex $argv 0]
			dump_parts $fname
		{% raw %}} {
		{% endraw %}
			error "Please Specify a file name"
			exit
		{% raw %}}
		{% endraw %}
	''',
	'dump_properties': r'''
		# {{spdx_license}}
		{{autogenerated}}

		{% raw %}proc dump_properties { fname partnum } {{% endraw %}

			set file [open $fname "w+"]
			set vivado_version [version -short]

			puts $file "{% raw %}{{% endraw %}"
			puts $file "\t\"vivado_version\": \"$vivado_version\", "
			puts $file "\t\"part\": \"$partnum\", "
			puts $file "\t\"properties\": {% raw %}{{% endraw %}"

			set part [get_parts $partnum]
			set properties [list_property $part]

			{% raw %}
			foreach property $properties {
			{% endraw %}
				set property_value [get_property $property $part]
				puts $file "\t\t\t\"$property\": \"$property_value\","
			{% raw %}
			}
			{% endraw %}

			# HACK: Ensure that the last property is empty to terminate the list
			puts $file "\t\t\t\"\":\"\""
			puts $file "\t{% raw %}}{% endraw %}"
			puts $file "{% raw %}}{% endraw %}"

		{% raw %}}{% endraw %}

		{% raw %}if { $argc == 2 } {
		{% endraw %}
			set fname [lindex $argv 0]
			set part [lindex $argv 1]
			dump_properties $fname $part
		{% raw %}} {
		{% endraw %}
			error "Please Specify a file name and a part number"
			exit
		{% raw %}}
		{% endraw %}
	''',
	'extract_tilemap': r'''
		# {{spdx_license}}
		{{autogenerated}}

		{% raw %}proc extract_tiles {{ fname }} {{% endraw %}
			set file [open $fname "w+"]

			# Emit opening curly-brace for JSON output
			puts $file "{% raw %}{{% endraw %}"
			puts $file "\t\"family\": \"{{family}}\","

			{% for name in device_names %}
			{{ '#'*100 }}
			# Create project for {{ name }}
			create_project -force -in_memory -name {{ family }}_{{name}}_{{package}} -part {{ (name, package, devices[name]) | part_number }}
			set_property DESIGN_MODE PinPlanning [get_filesets sources_1]
			# Open the design in IO Planning mode
			open_io_design

			puts $file "\t\"{{name}}\": {{ '{' }}"
			puts $file "\t\t\"tiles\": \["
			{% raw %}
			# Extract tiles from device
			if { ![catch {set tiles [get_tiles -verbose]} err]} {
			{% endraw %}
				{% raw %}
				foreach tile $tiles {
				{% endraw %}
					puts $file "\t\t\t\"$tile\","
				{% raw %}
				}
				{% endraw %}
				# HACK: Ensure that the last item is empty to terminate the list
				puts $file "\t\t\t\"\""
			{% raw %}
			}
			{% endraw %}
			puts $file "\t\t\],"
			puts $file "\t\t\"clock_regions\": \["
			{% raw %}
			# Extract clock regions from device
			if { ![catch {set clocks [get_clock_regions -verbose]} err]} {
			{% endraw %}
				{% raw %}
				foreach clock $clocks {
				{% endraw %}
					puts $file "\t\t\t\"$clock\","
				{% raw %}
				}
				{% endraw %}
				# HACK: Ensure that the last item is empty to terminate the list
				puts $file "\t\t\t\"\""
			{% raw %}
			}
			{% endraw %}
			puts $file "\t\t\]"

			close_project
			puts $file "\t{{ '}' }}{% if not loop.last %},{% endif %}"
			{% if loop.last %}
			{{ '#'*100 }}
			{% endif %}
			{% endfor %}

			# Emit closing curly-brace for JSON output
			puts $file "{% raw %}}{% endraw %}"

		{% raw %}}{% endraw %}

		{% raw %}if { $argc == 1 } {
		{% endraw %}
			set fname [lindex $argv 0]
			extract_tiles $fname
		{% raw %}} {
		{% endraw %}
			error "Please Specify a file name"
			exit
		{% raw %}}
		{% endraw %}
	'''
}




def render_template(template_name, *, filters = None, **kwargs) -> str:
	def autogen_message() -> str:
		return textwrap.dedent(f'''\
			#########################################
			# THIS FILE WAS AUTOGENERATED BY XYLENE #
			# { datetime.now().isoformat().center(37) } #
			#          !!! DO NOT EDIT !!!          #
			#  !!! CHANGES WILL BE OVERWRITTEN !!!  #
			#########################################

			# To run manually:
			# vivado -mode batch -source <SCRIPT_NAME>.tcl -tclargs parts.json
		''').strip()


	def tcl_escape(string : str) -> str:
		return '{' + re.sub(r'([{}\\])', r'\\\1') + '}'

	def tcl_quote(string : str) -> str:
		return '"' + re.sub(r'([$[\\])', r'\\\1') + '"'


	if template_name not in TEMPLATES:
		raise ValueError(f'Unknown template \'{template_name}\'')

	template = textwrap.dedent(
		TEMPLATES.get(template_name)
	).strip()

	env = Environment(
		trim_blocks   = True,
		lstrip_blocks = True
	)

	env.filters['tcl_escape'] = tcl_escape
	env.filters['tcl_quote']  = tcl_quote

	if filters is not None:
		env.filters.update(filters)

	compiled_template = env.from_string(
		template,
		globals = {
			'spdx_license' : 'SPDX-License-Identifier: BSD-3-Clause',
			'autogenerated': autogen_message(),
			'now'          : datetime.utcnow
		}
	)

	return compiled_template.render(
		**kwargs
	)
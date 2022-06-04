# SPDX-License-Identifier: BSD-3-Clause
import os, sys, datetime
sys.path.insert(0, os.path.abspath('.'))


version   = 'latest' # :nocov:
project   = 'prjxylene'
release   = version.split('+')[0]
copyright = f'{datetime.date.today().year}, Aki "lethalbit" Van Ness, et. al.'
language  = 'en'

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.githubpages',
	'sphinx.ext.graphviz',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'sphinxcontrib.mermaid',
	'sphinxcontrib.platformpicker',
	'sphinxcontrib.wavedrom',
	'myst_parser',
	'sphinx_construct',
	'sphinx_rtd_theme',
]

source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

pygments_style         = 'monokai'
autodoc_member_order   = 'bysource'
graphviz_output_format = 'svg'
todo_include_todos     = True

intersphinx_mapping = {
	'python'   : ('https://docs.python.org/3', None),
	'construct': ('https://construct.readthedocs.io/en/latest', None),
}

napoleon_google_docstring = False
napoleon_numpy_docstring  = True
napoleon_use_ivar         = True
napoleon_custom_sections  = ["Platform overrides"]



html_baseurl     = ''
html_theme       = 'sphinx_rtd_theme'
html_copy_source = False

html_theme_options = {
	'collapse_navigation' : False,
	'style_external_links': True,
}

html_static_path = [
	'_static'
]

html_css_files = [
	'css/styles.css'
]

html_js_files = [
	'js/mermaid.min.js',
	'js/wavedrom.min.js',
	'js/wavedrom.skin.js',
]

html_style = 'css/styles.css'

autosectionlabel_prefix_document = True
# Disable CDN so we use the local copy
mermaid_version = ''

offline_skin_js_path = '_static/js/wavedrom.skin.js'
offline_wavedrom_js_path = '_static/js/wavedrom.min.js'

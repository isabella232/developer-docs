# -*- coding: utf-8 -*-
#
# invoca documentation build configuration file, created by
# sphinx-quickstart on Fri May  9 18:53:36 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import re
import pickle
from datetime import datetime
# append the current folder to the Python class path
sys.path.append(os.getcwd())
from doc_versions import *

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# is this file being executed on read the docs or locally?
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# these templates will only be used we building locally, they will be ignored by RTD
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = ['.rst']

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Invoca'
copyright = u'{}, Invoca'.format(datetime.now().year)

# The full version, including alpha/beta/rc tags.
version = COMMON_VERSION
release = COMMON_VERSION

if on_rtd:
  custom_template_path = './custom_templates/'
  source_path = './'
else:
  custom_template_path = './source/custom_templates/'
  source_path = './source/'

"""
Replaces directives with the contents of a custom template. Substitutes
values from the directive into the template.

Example directive:
.. api_endpoint::
  :verb: GET
  :path: /advertiser_campaigns
  :description: Get all campaigns for an Advertiser
  :page: get_advertiser_campaigns

Example template:
<div class=":verb:">:description</div>
"""
def build_template(match, template_file_name):
  lines = match.group().splitlines()

  # remove the directive line
  lines.pop(0)

  # extract the replacement keys and values
  template_vars = {}
  for line in lines:
    if not line.strip(): continue
    args = line.strip().split(' ')
    key = args.pop(0)
    template_vars[key] = ' '.join(args)

  # open the template and find/replace the keys with the values
  template = open('{}{}'.format(custom_template_path, template_file_name), 'r').read()
  for search, replacement in template_vars.iteritems():
    if re.search(search, template):
      template = template.replace(search, replacement)
    else:
      raise Exception("Template does not have replacement key " + search)

  # raise error if we have extra or not enough keys
  remaining_keys = re.search(r":[a-zA-Z_]+:", template)
  if not remaining_keys:
    return template
  else:
    raise Exception("Template has unreplaced key " + remaining_keys.group())


def find_and_replace_templates(source, directive_name, template_file_name):
  return re.sub(
          re.compile("^ *\.\. {}::$\n(^\s+:\w+:\s+.*$\n)+^$\n".format(directive_name), re.MULTILINE),
          lambda match: build_template(match, template_file_name),
          source)


def build_api_endpoint_template(source):
  return find_and_replace_templates(source, "api_endpoint", "_api_endpoint.rst")


# Replace version symbols with actual version numbers
# Version numbers are defined in doc_versions.py
def source_handler(app, docname, source):
  source[0] = build_api_endpoint_template(source[0])

  for symbol_string, version_string in VERSIONS.iteritems():
    source[0] = re.sub(symbol_string, version_string, source[0])

def build_partials(app, env, docnames):
  for docname in env.found_docs:
    if re.search(r"/_[^/]+$", docname) and not re.search('custom_template', docname):
      print docname
      partial = open('{}{}{}'.format(source_path, docname, '.rst'), 'r').read()
      for symbol_string, version_string in VERSIONS.iteritems():
        partial = re.sub(symbol_string, version_string, partial)
      new_docname = docname + '.tmp'
      open('{}{}'.format(source_path, new_docname), 'w').write(partial)

def setup(app):
  app.connect('env-before-read-docs', build_partials)
  app.connect('source-read', source_handler)
  app.add_javascript('js/custom.js')
  app.add_javascript('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js')
  app.add_stylesheet('css/custom.css')


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# Uncomment the following lines to build the docs locally using sphinx-build
if not on_rtd:  # only import and set the theme if we're building docs locally
  import sphinx_rtd_theme
  html_theme = 'sphinx_rtd_theme'
  html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_context = {}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {"nosidebar": True, "display_version": False, "logo_only": True}

# It seems that ReadTheDocs ignores html_theme_options above, so here we are expanding the options directly into the context
if on_rtd:
  for key in html_theme_options:
    html_context['theme_' + key] = html_theme_options[key]

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = ''

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/logo.png'

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'invocadoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'invoca.tex', u'invoca Documentation',
   u'invoca', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '_static/logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'invoca', u'invoca Documentation',
     [u'invoca'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'invoca', u'invoca Documentation',
   u'invoca', 'invoca', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False

rst_prolog = """

.. title:: Invoca Developer Portal
.. raw:: html

  <div style="text-align: right;" >
    <a href="http://www.invoca.net/home">Return to the Invoca Platform</a>
  </div>


"""

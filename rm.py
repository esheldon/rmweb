#!/usr/bin/env python2.7

import os
import cgi
import rm_util


print "Content-type: text/html\n\n"
print

fs = cgi.FieldStorage()

rm_util.print_head(rm_util.vers)
rm_util.print_title()

rm_util.print_search_form(fs)

rm_util.print_main_table(fs)


#!/usr/bin/env python2.7

import rm_util
import cgi

print "Content-type: text/html\n\n"
print

fs = cgi.FieldStorage()

if 'id' not in fs:
    print "You must send an id"
else:
    cluster=rm_util.get_cluster(fs['id'].value)
    comments=cluster.data['comments']

    print "<form action='update.py'>"
    print "    Comments<br>"
    print "    <textarea rows=20 cols=79 name='comments'>%s</textarea>" % comments
    print "    <br>"
    print "    <input type='hidden' name='id' value='%s'>" % fs['id'].value
    print "    <input type='submit' value='Submit'>"
    print "</form>"
 


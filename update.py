#!/usr/bin/env python2.7

import rm_util
import cgi

print "Content-type: text/html\n\n"
print

fs = cgi.FieldStorage()

if 'id' not in fs:
    print "You must send an id"
else:
    comments=fs.getfirst('comments','')
    cluster=rm_util.get_cluster(fs['id'].value)
    cluster.update_comments(comments)


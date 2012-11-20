import urllib
from collections import OrderedDict
import sqlite_util

vers='redmapper-dr8-4.15-lgt20'
dbfile='%s.db' % vers
tbname='rm'

dbname="RedMapper Clusters"
idname='mem_match_id'
default_field='lambda_chisq'
row_fields=OrderedDict([('mem_match_id', {'fmt':'%s'}),
                        ('ra',           {'fmt':'%s'}),
                        ('dec',          {'fmt':'%s'}),
                        ('maskfrac',     {'fmt':'%.3f'}),
                        ('imag',         {'fmt':'%.2f'}),
                        ('p_cen_0',      {'fmt':'%.3f'}),
                        ('lambda_chisq', {'fmt':'%.2f'}),
                        ('bcg_spec_z',   {'fmt':'%.3f'}),
                        ('z_lambda',     {'fmt':'%.3f'})])

default_limit='100'

def print_head(title, type='cluster'):
    print "<Head>"

    if type=='rm':
        print "<link rel='STYLESHEET' href='styles/rm.css' type='text/css'>"
    else:
        print "<link rel='STYLESHEET' href='styles/cluster.css' type='text/css'>"
    print "<TITLE>",title,"</TITLE>"
    print "</Head>"

def print_title():
    print '<h1><a href="./rm.py">RedMapper Clusters</a>:',vers,'</h1>'

def wln(*args):
    for a in args:
        print a,
    print '<br>'


def print_top_row():
    print '<tr>'
    for k in row_fields:
        print '<th>'
        print k
        print '</th>'

    print '<th>info</th>'
    print '<th>explore</th>'
    print '</tr>'

def print_th_row():
    print '<tr>'
    for k in row_fields:
        print '<td class="mid">'
        print k
        print '</td>'

    print '<td class="mid">info</td>'
    print '<td class="mid">navi</td>'
    print '<td class="mid">chart</td>'
    print '</tr>'

def get_navi_url(ra,dec):
    #url='http://skyserver.sdss3.org/dr9/en/tools/chart/navi.asp?opt=S&ra=%s&dec=%s'
    #url = url % (ra,dec)
    url='http://skyserver.sdss3.org/dr9/en/tools/chart/navi.asp?'
    queries={'ra':ra,'dec':dec,'opt':'S'}
    return url + urllib.urlencode(queries)

def get_fchart_url(ra,dec,full=False):
    #url='http://skyservice.pha.jhu.edu/DR9/ImgCutout/getjpeg.aspx?ra=%(ra)s&dec=%(dec)s&scale=0.7922&width=512&height=512&opt=&query=%(query)s'
    #url='http://skyservice.pha.jhu.edu/DR9/ImgCutout/getjpeg.aspx?'
    if full:
        url='http://skyserver.sdss3.org/dr9/en/tools/chart/chart.asp?'
        scale=0.619
        width=800
        height=800
    else:
        #url='http://skyservice.pha.jhu.edu/DR8/ImgCutout/getjpeg.aspx?'
        url='http://skyservice.pha.jhu.edu/DR9/ImgCutout/getjpeg.aspx?'
        scale=0.792
        width=512
        height=512

    query="""
    RA DEC
    %(ra)s %(dec)s
    """.strip()
    query=query % {'ra':ra,'dec':dec}

    queries={'ra':ra,'dec':dec,'query':query,'scale':scale,'width':width,'height':height,'opt':'S'}
    return url + urllib.urlencode(queries)

def get_ned_url(ra, dec):
    # ned doesn't accept high precision longitude
    lon = '%.4f' % ra
    lat = '%.6f' % dec
    radius = '0.16667'
    url='http://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon={lon}d&lat={lat}d&radius={radius}&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&nmp_op=ANY&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'
    url=url.format(lon=lon, lat=lat, radius=radius)

    return url

class Cluster:
    def __init__(self, data):
        self.data=data

    def print_row(self):


        print '<tr>'
        for k in row_fields:
            print '  <td>'
            print '  '+row_fields[k]['fmt'] % self.data[k]
            print '  </td>'

        id=self.data[idname]
        info_url='./cluster2html.py?id=%s' % id
        navi_url=get_navi_url(self.data['ra'], self.data['dec'])
        fchart_url = get_fchart_url(self.data['ra'], self.data['dec'],full=True)
        print '<td><a target="_blank" href="%s">open</a></td>' % info_url
        print '<td><a target="_blank" href="%s">open</a></td>' % navi_url
        print '<td><a target="_blank" href="%s">open</a></td>' % fchart_url

        print '</tr>'

    
    def tohtml(self):

        id=self.data[idname]
        main=['mem_match_id',
              'ra','dec',
              'lambda_chisq',
              'p_bcg_0',
              'p_cen_0',
              'imag',
              'z_lambda',
              'bcg_spec_z',
              'maskfrac',
              'umg','gmr','rmi','imz',
              'comments']
        navi=get_navi_url(self.data['ra'], self.data['dec'])
        fchart=get_fchart_url(self.data['ra'], self.data['dec'])
        fchart_full=get_fchart_url(self.data['ra'], self.data['dec'],full=True)
        ned=get_ned_url(self.data['ra'], self.data['dec'])

        tit='cluster: %s' % id
        print_head(tit, type='cluster')

        mainurl = "<a href='./rm.py'>"+dbname+"</a>"

        editlink = "<a target='_blank' href='./edit.py?id=%s'>Edit comments</a>" % id
        findlink = "<a target='_blank' href='%s'>finding chart</a>" % fchart_full
        navilink = "<a target='_blank' href='%s'>navigate</a>" % navi
        nedlink = "<a target='_blank' href='%s'>ned</a>" % ned

        link_list="%s | %s | %s | %s" % (findlink,navilink,nedlink,editlink)

        print "         <table class='cluster' width=1000>"
        print "           <tr>"
        print "             <td align='left'>"
        print "               <font size=5>"+mainurl+"</font>"
        print "             </td>"
        print "             <td align='right'>"
        print "               "+link_list
        print "             </td>"
        print "           </tr>"
        print "           <tr>"
        print "             <td>"
        print "               <table class='cluster'>"

        for k in main:
            print '                 <tr><td><b>%s</b>: </td><td>%s</td></tr>' % (k,self.data[k])

        print "               </table>"
        print "             </td>"
        print "             <td valign=top align=right>"
        print "               <a target='_blank' href='%s'><img src='%s'></a><br>" % (fchart_full,fchart)
        print "             </td>"
        print "           </tr>"
        print "           <tr><td>Other data</td><td></td></tr>"
        print "           <tr>"
        print "             <td>"
        print "               <table class='cluster'>"
        for k in self.data.keys():
            if k not in main:
                print '        <tr><td><b>%s</b>:</td><td>%s</td></tr>' % (k,self.data[k])

        print "               </table>" 
        print "             </td>"
        print "           </tr>"
        print "         </table>"

    def update_comments(self, comments):
        id=self.data[idname]

        query="""
        update 
            %(tbname)s
        set 
            comments=?
        where
            %(idname)s = %(id)s

        """ % {'tbname':tbname,'idname':idname,
               'id':id}

        try:
            with sqlite_util.SqliteConnection(dbfile) as conn:
                #c=conn.execute(query)
                curs=conn.cursor()
                curs.execute(query, (comments,))
                print "Successfully updated cluster: ",id,"<br>" 

        except:
            print "Failed to update cluster: ",id,"<br>"
            print "Error info: ",sys.exc_info(),"<br>"
        print_close_window()

def print_close_window():
    print '<form method="post">'
    print '<input type="button" value="close window" onClick="window.close();">'
    print '</form>'



def get_cluster(id):
    cluster=None
    with sqlite_util.SqliteConnection(dbfile) as conn:
        query="select * from %s where %s=%s" % (tbname,idname,id)
        c=conn.execute(query)
        data=c.fetchall()
        if len(data) == 0:
            wln("did not find cluster with %s=%s" % (idname,id))
        else:
            cluster=Cluster(data[0])
    return cluster

def get_nperpage(fs):
    nperpage=fs.getfirst('nperpage',100)
    try:
        nperpage=int(nperpage)
    except:
        nperpage=100
    return nperpage

def get_page(fs):
    page=fs.getfirst('page',1)
    try:
        page=int(page)
    except:
        page=1
    return page

def get_limit(fs):
    limit=fs.getfirst('limit',default_limit)
    if limit == '':
        limit='all'
    return limit

def print_search_form(fs):
    if fs.has_key('pattern'):
        pattern = fs['pattern'].value
    else:
        pattern=''

    nperpage=get_nperpage(fs)
    page=get_page(fs)

    if 'orderby' in fs:
        default_field=fs['orderby'].value
    else:
        default_field=_default_orderby
    if 'sortorder' in fs:
        default_sortorder=fs['sortorder'].value
    else:
        if default_field in _default_sortorder:
            default_sortorder=_default_sortorder[default_field]
        else:
            default_sortorder=_default_sortorder['default']

    if default_sortorder == 'ASC':
        other_sortorder='DESC'
    else:
        other_sortorder='ASC'


    print "<form action='rm.py'>"
    print "    Sort by"
    print "    <select name='orderby'>"
    for k in row_fields:
        if default_field == k:
            print "        <option selected value='"+k+"'>",k
        else:
            print "        <option value='"+k+"'>",k
    print "    </select>"
    print "    <select name='sortorder'>"
    print "        <option selected value='{order}'>{order}".format(order=default_sortorder)
    print "        <option value='{order}'>{order}".format(order=other_sortorder)
    print "    </select>"
    print "<br>"
    print "    show <input size=6 type='text' name='nperpage' value=%s> per page " % nperpage
    print "    current page <input size=6 type='text' name='page' value=%s> " % page

    print "<br>"
    print "    Search <a target='_blank' href='examples.html'>(example searches)</a><br>"
    print "    <textarea rows=3 cols=79 name='pattern'>%s</textarea>" % pattern
    print "    <input type='submit' value='Submit'>"
    print "</form>"
    print "<p>"



_default_orderby='lambda_chisq'
_default_sortorder = {'lambda_chisq':'DESC',
                      'default':'ASC'}
def print_main_table(fs, **keys):
    with sqlite_util.SqliteConnection(dbfile) as conn:

        if 'orderby' in fs:
            orderby=fs['orderby'].value
        else:
            orderby=_default_orderby

        if 'sortorder' in fs:
            sortorder=fs['sortorder'].value
        else:
            if orderby in _default_sortorder:
                sortorder=_default_sortorder[orderby]
            else:
                sortorder=_default_sortorder['default']
 
        if 'pattern' in fs:
            pattern=fs['pattern'].value
            query="select * from %(tbname)s where %(pattern)s order by %(orderby)s %(sortorder)s %(limits)s"
        else:
            pattern=''
            query="select * from %(tbname)s order by %(orderby)s %(sortorder)s %(limits)s"

        nperpage=get_nperpage(fs)
        page=get_page(fs)

        start=(page-1)*nperpage
        limits = "limit %s, %s" % (start, nperpage)

        query=query % {'tbname':tbname,'pattern':pattern,'orderby':orderby,'sortorder':sortorder,'limits':limits}
        c=conn.execute(query)

        print " <table class='main'>"
        for i,row in enumerate(c):
            if (i % 15) == 0:
                print_th_row()

            cluster = Cluster(row)
            cluster.print_row()
        print "</table>"



﻿from django.template.loader import get_template
from django.conf import settings
from myobj import conf as MYCONF
from django.template import Context, Template
from django import template
from django.utils import importlib
from myobj import utils
register = template.Library()
from django.db import connection
import time
@register.filter(name='handle')

def handle(value, paramscms):
    start_time = time.time()
    handle.countiter = (handle.countiter + 1) if utils.isthereattr(handle, 'countiter') else 1
    handle.handlesnav = handle.handlesnav if utils.isthereattr(handle, 'handlesnav') else paramscms['itemnav'].links('handle_system')
    handle.handleobj = handle.handleobj if utils.isthereattr(handle, 'handleobj') else dict([(objh.name, {'view': objh.links('views_system',False),'grouplist': [objgroup.name for objgroup in objh.links('views_system',False).links('group_system')],'template': objh.links('template_system',False)}) for objh in handle.handlesnav.select_related().all()])
    
    #permission
    blokview = True
    for idmygroup in paramscms['request'].mygrouplist:
        if(idmygroup in handle.handleobj[value]['grouplist']):
            blokview = False
            break
    #if there are no groups that show
    if(blokview == True and len(handle.handleobj[value]['grouplist']) != 0): return ''
    viewobj = handle.handleobj[value]['view']
    templateobj = handle.handleobj[value]['template']
    
    namemodul = viewobj.propertiesdict['importmodul_system']
    nameview = viewobj.propertiesdict['nameimport_view_system']
    patchtemplate = templateobj.propertiesdict['patch_tamplate_system']
    
    startlenq = len(connection.queries)
    
    getmodul = importlib.import_module(namemodul)
    linkfunk = getmodul.__getattribute__(nameview)
    
    datacontext = linkfunk(paramscms)
    querydictend = connection.queries
    strsqlq = ''
    if(settings.DEBUG == True and MYCONF.DEBUGSQL == True):
        timeallsql = 0
        for sqlline in querydictend[startlenq:]:
            timeallsql += float(sqlline['time'])
        if(len(querydictend[startlenq:]) > 0):
            strsqlq = "'SQL': [\n\t" + "\n\t".join(["{'time': '" + dictp['time'] + "', 'sql': '" + dictp['sql'] + "'}," for dictp in querydictend[startlenq:]]) + "\n], 'countQ': " + str(len(querydictend[startlenq:])) + ", 'timeQ': " + str(timeallsql)
    
    t = get_template(patchtemplate) if (templateobj.propertiesdict['isbd_tamplate_system'] == 'False') else Template(templateobj.propertiesdict['html_tamplate_system'])
    html = t.render(Context({'datacontext': datacontext}))
    #tracing
    end_time = time.time()
    tracing = "\n{'view': 'nview: " + namemodul + "." + nameview + "(L" + str(viewobj.id) + "), ntempl: " + patchtemplate + "(L" + str(templateobj.id) + "), time: " + str(("%.3f" % (end_time - start_time))) + "', \n" + strsqlq + "\n},"
    if(utils.isthereattr(handle, 'tracingstr')):
        handle.tracingstr += tracing
    else: handle.tracingstr = tracing
    
    if(handle.countiter == paramscms['counthand']):
        if(settings.DEBUG == True):
            html += "<script>var tracingsys = [" + handle.tracingstr + "];</script>"
            del handle.tracingstr
        
        del handle.countiter
        del handle.handlesnav
        del handle.handleobj
    
    return html
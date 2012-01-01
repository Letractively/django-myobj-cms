﻿from django.shortcuts import render_to_response
from myobj.conf import NAVENTRY, getusergrouplist
from myobj.models import uClasses
from django.conf import settings
from django.template import loader, VariableNode

def getpage(request, *args, **kwargs):
    #get urls
    actionurl = [pr for pr in request.path_info.split('/') if pr != '']
    classmenu = uClasses.objects.get(codename='menu_system')
    itemnav = actionurl[1] if (NAVENTRY != '') else actionurl[0]

    if(str(itemnav).isdigit()):
        objmenu = classmenu.getobjects(id=itemnav)
    else:
        objmenu = classmenu.getobjprop(codename_system=itemnav)
    mythisnav = objmenu[0]
    templateobj = mythisnav.links('template_system',False)
    request.__setattr__('mygrouplist', getusergrouplist(requestobj = request))
    counthandles = 0
    if(settings.DEBUG == True):
        tempt = loader.get_template(templateobj.propertiesdict['patch_tamplate_system'])
        for variable in tempt.nodelist.get_nodes_by_type(VariableNode):
            token = variable.filter_expression.token
            indh = token.find('|handle:')
            if(indh != -1):
                counthandles += 1
    return render_to_response(templateobj.propertiesdict['patch_tamplate_system'], {'paramsreq': {'counthand': counthandles,'request': request, 'itemnav': mythisnav, 'actionurl': actionurl}})


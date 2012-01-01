from myobj import conf as MYCONF

PROPN = [
    'codename','name','description','myfield','minfield','maxfield','required','udefault'
]
PROPL = [
    ['codename_system',       'codename_system','codename system',1,'','','False',''],
    [MYCONF.PROP_PATCH_TEMPLATE_SYS, 'patch_system','patch system',1,'','','True',''],
    ['importmodul_system',    'importmodul_system','import modul system',1,'','','True',''],
    ['nameimport_view_system','nameimport_view_system','name import view system',1,'','','False',''],
    ['description_system',    'description_system','description system',2,'','','False',''],
    [MYCONF.PROP_NAME_PARENT_MENU,    MYCONF.PROP_NAME_PARENT_MENU,'parent element nav system',3,'','','True',0],
]

ClASSN = [
    'codename','name','description','tablespace','properties','aggregation'
]
CLASSL = [
    ['template_system', 'template_system','template system',2,MYCONF.PROP_PATCH_TEMPLATE_SYS,''],
    [MYCONF.CLASS_NAME_VIEWS,    MYCONF.CLASS_NAME_VIEWS,'views system',2,'importmodul_system,nameimport_view_system,description_system',''],
    [MYCONF.CLASS_NAME_HANDLE,   MYCONF.CLASS_NAME_HANDLE,'handle system',2,'',MYCONF.CLASS_NAME_VIEWS + ',template_system'],
    [MYCONF.PROP_PARAMSNAV_SYS,   MYCONF.PROP_PARAMSNAV_SYS,'params system',2,'codename_system,description_system',''],
    [MYCONF.CLASS_NAME_MENU, MYCONF.CLASS_NAME_MENU,'menu system',2,'codename_system,description_system,' + MYCONF.PROP_NAME_PARENT_MENU,'template_system,' + MYCONF.CLASS_NAME_HANDLE + ',' + MYCONF.PROP_PARAMSNAV_SYS],
    [MYCONF.CLASS_NAME_GROUP, MYCONF.CLASS_NAME_GROUP,'group system',2,'codename_system',MYCONF.CLASS_NAME_VIEWS],
]

listadminpropsview = [name[0] for name in PROPL]
listadminclassview = [name[0] for name in CLASSL]
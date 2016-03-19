import re
from urllib.parse import urljoin
# def csea_exceptions(link) :
#     if(link.startswith('http://csea.iitg.ernet.in') and link.endswith('-')) :
#         pattern = re.compile('http://csea.iitg.ernet.in/csea/Public/web_new/index.php/activities/([a-zA-Z-_0-9]+)/.*')
#         matching = pattern.match(link)
#         if(matching.group(1) != None) :
#             return 'http://csea.iitg.ernet.in/csea/Public/web_new/index.php/activities/' + matching.group(1)
#         else :
#             return link
#     else :
#         return link

def is_intranet_link(link) :
    if link == None :
         return False
    else :
        refined = link[7:]
        if refined.startswith('iitg.ernet.in') or refined.startswith('www.iitg.ernet.in') :
            return True
        else :
            if refined[refined.find('.')+1:].startswith('iitg.ernet.in') :
                return True
            else :
                return False

def relativeLinkFilter(link , ext) :
    if link != None and ext != None :
        if not ('#' in ext) :
            return True
        else :
            ind = ext.find('#')
            if ind == 0 :
                return False
            if not link.endswith(ext[:ind])                 :
                return True
            else :
                return False
    elif ext == None and link != None :
        return True
    else :
        return False

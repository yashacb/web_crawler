import re
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
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
        if link.startswith('https://') :
            refined = link[8:]
        else :
            refined = link[7:]
        if refined.startswith('iitg.ernet.in') or refined.startswith('www.iitg.ernet.in') :
            return True
        else :
            if refined[refined.find('.')+1:].startswith('iitg.ernet.in') :
                return True
            else :
                return False

def link_check(link , actual_link) :
    return actual_link != None and (not actual_link.startswith('http://csea.iitg.ernet.in/csea/Public/web_new/index.php/activities')) \
    and (not link.startswith('http://intranet.iitg.ernet.in/eventcal/')) \
    and (not link.startswith('http://shilloi.iitg.ernet.in/~hss/reservation')) and is_intranet_link(actual_link) \
    and (not actual_link.startswith('http://jatinga.iitg.ernet.in/~dppc/resources/resources/')) and len(actual_link) <= 200 \
    and (not actual_link.startswith('http://jatinga.iitg.ernet.in/cseforum/calendar.php'))

# Returns false if link appended with ext is the same as link .
def relativeLinkFilter(link , ext) :
    if link != None and ext != None :
        if not ('#' in ext) :
            return True
        else :
            ind = ext.find('#')
            if ind == 0 :
                return False
            else :
                complete = urljoin(link , ext[:ind])
                if complete != link and complete.count('#') <= 1 :
                    return True
                else :
                    return False
    elif ext == None and link != None :
        return True
    else :
        return False

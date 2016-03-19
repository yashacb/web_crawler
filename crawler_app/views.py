from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from bs4 import BeautifulSoup
import urllib.request
import ssl
from . import functions
from socket import timeout
import urllib.error
from urllib.parse import urljoin
import re
import time

def index(request) :
    form = SearchForm()
    print(functions.make_link('/~dupc' , 'http://jatinga.iitg.ernet.in/cseintranet'))
    return render(request , 'crawler_app/index.html' , {'form' : form})

def crawl(request) :
    start_time = time.time()
    default_url = 'http://intranet.iitg.ernet.in' ;
    visited = {None} ;
    pdfs = {None} ;
    unvisited = {default_url}
    while unvisited :
        link = unvisited.pop()
        try :
            if(link != None) and (not link in visited) :
                visited.add(link)
                open_connection = urllib.request.urlopen(link , timeout = 1)
                connection_info = open_connection.info()
                if 'text/html' in connection_info['Content-Type'] :
                    bsoup = BeautifulSoup(open_connection.read())
                    print(link)
                    all_links = bsoup.find_all('a')
                    for li in all_links :
                        ext = li.get('href')
                        if ext != None and ext != '' and (functions.relativeLinkFilter(link , ext)) and (not ext.startswith('mailto:')) :
                            actual_link = urljoin(link , ext)
                            if actual_link != None and (not actual_link.startswith('http://csea.iitg.ernet.in/csea/Public/web_new/index.php/activities')) \
                            and (not actual_link in visited) and (not link.startswith('http://intranet.iitg.ernet.in/eventcal/')) \
                            and (not link.startswith('http://shilloi.iitg.ernet.in/~hss/reservation')) and functions.is_intranet_link(actual_link) \
                            and (not actual_link.startswith('http://jatinga.iitg.ernet.in/~dppc/resources/resources/')) and len(actual_link) <= 200 \
                            and (not actual_link.startswith('http://jatinga.iitg.ernet.in/cseforum/calendar.php')) :
                                unvisited.add(actual_link)
        except timeout :
            print('Timeout : ' + link)
        except urllib.error.URLError as e :
            print(str(e) + " : " + link)
        except (TypeError , IndexError , UnicodeEncodeError) as err :
            print(str(err))
        except :
            print('Some other error : ' + link)
    print(len(visited))
    print(time.time() - start_time)
    string = 'Time taken : ' + str(time.time() - start_time) + '<br>'
    for l in visited :
        string = string + str(l) + '<br>'
    return HttpResponse('Crawled links : <br> '+ str(len(visited)) + '<br>' + string)

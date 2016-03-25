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
import pickle

def index(request) :
    form = SearchForm()
    print(functions.make_link('/~dupc' , 'http://jatinga.iitg.ernet.in/cseintranet'))
    return render(request , 'crawler_app/index.html' , {'form' : form})

def crawl(request) :
    start_time = time.time()
    default_url = 'http://intranet.iitg.ernet.in' ;
    visited = {None}
    text = {None}
    pdfs = {None}
    images = {None}
    others = {None}
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
                    text.add(link[:len(link) if (not '#' in link) else link.find('#')])
                    # All 'a' tags
                    all_links = bsoup.find_all('a')
                    for li in all_links :
                        ext = li.get('href')
                        if ext != None and ext != '' and (functions.relativeLinkFilter(link , ext)) and (not ext.startswith('mailto:')) :
                            actual_link = urljoin(link , ext)
                            if functions.link_check(link , actual_link) and (not actual_link in visited) :
                                actual_link = urllib.parse.quote(actual_link.strip() , safe="%/:=&?~#+!$,;'@()*[]")
                                unvisited.add(actual_link)
                    # End
                    # All frame tags
                    frame_links = bsoup.find_all('frame')
                    for li in frame_links :
                        ext = li.get('src')
                        if ext != None and ext != '' and functions.relativeLinkFilter(link , ext) and (not ext.startswith('mailto:')) :
                            actual_link = urljoin(link , ext)
                        if functions.link_check(link , actual_link) and (not actual_link in visited) :
                            actual_link = urllib.parse.quote(actual_link.strip() , safe="%/:=&?~#+!$,;'@()*[]")
                            unvisited.add(actual_link)
                    # End
                    # All iframe tags
                    frame_links = bsoup.find_all('iframe')
                    for li in frame_links :
                        ext = li.get('src')
                        if ext != None and ext != '' and functions.relativeLinkFilter(link , ext) and (not ext.startswith('mailto:')) :
                            actual_link = urljoin(link , ext)
                        if functions.link_check(link , actual_link) and (not actual_link in visited) :
                            actual_link = urllib.parse.quote(actual_link.strip() , safe="%/:=&?~#+!$,;'@()*[]")
                            unvisited.add(actual_link)
                    # End
                # For documents
                elif ('application/pdf' in connection_info['Content-Type']) or ('application/msword' in connection_info['Content-Type']) or \
                ('application/vnd.openxmlformats-officedocument.wordprocessingml.document' in connection_info['Content-Type']) or \
                ('application/vnd.ms-excel' in connection_info['Content-Type']) or \
                ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in connection_info['Content-Type']) or \
                ('application/vnd.ms-powerpoint' in connection_info['Content-Type']) or \
                ('application/vnd.openxmlformats-officedocument.presentationml.presentation' in connection_info['Content-Type']) and \
                functions.is_intranet_link(link) :
                    link = urllib.parse.quote(link.strip() , safe="%/:=&?~#+!$,;'@()*[]")
                    pdfs.add(link)
                # End
                else :
                    link = urllib.parse.quote(link.strip() , safe="%/:=&?~#+!$,;'@()*[]")
                    others.add(link)

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
    string = 'Time taken : ' + str(time.time() - start_time) + '<br>' + 'HTML pages : ' + str(len(text)) + '<br>'
    for l in text :
        string = string + str(l) + '<br>'
    string += 'PDF pages : ' + str(len(pdfs)) + '<br>'
    for l in pdfs :
        string = string + str(l) + '<br>'
    string += 'Other links : ' + str(len(others)) + '<br>'
    for l in others :
        string = string + str(l) + '<br>'
    try :
        html_file = open('/home/yashwanthbetha/html.txt' , 'wb')
        pdf_file = open('/home/yashwanthbetha/pdf.txt' , 'wb')
        other_file = open('/home/yashwanthbetha/other.txt' , 'wb')
        pickle.dump(text , html_file)
        pickle.dump(pdfs , pdf_file)
        pickle.dump(others , other_file)
        html_file.close()
        pdf_file.close()
        other_file.close()
    except :
        print('Error in file handling .')
    return HttpResponse('Crawled links : <br> '+ str(len(visited)) + '<br>' + string)

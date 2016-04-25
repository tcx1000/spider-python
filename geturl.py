#coding=utf-8

import urllib
import re
import sys
import random
import socket
import urllib2
import cookielib
import time


class BrowserBase(object): 

    def __init__(self):
        
        socket.setdefaulttimeout(20)

    
    def speak(self,name,content):
        
        print '[%s]%s' %(name,content)

    
    def openurl(self,url):

        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
                    ] 
       
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
        try:
            res = self.opener.open(url)
           # print res.read()
        except Exception,e:
            self.speak(str(e),url)
        else:
            return res


def getHtml(url):

    spider = BrowserBase()
    page = spider.openurl(url)
    html = page.read()

    return html


def getInfo(html,location):

    pub_info = re.findall(r'<a href=".*" title=".*'+location+'.*" class="">',html)
    pub_date = re.findall(r'<td nowrap="nowrap" class="time">.*</td>',html)

    count=0
    for info in pub_info:
    	new_info = info + pub_date[count]
    	pub_info[count] = new_info
        count=count+1

    return pub_info

def getDetail(url):

	page = urllib.urlopen(url)
	html = page.read()
	detail = []
	detail.append(re.findall(r'<span class="color-green">(.*)</span>',html))
	detail.append(re.findall(r'<span class="from">来自: <a href="https://www.douban.com/people/121015832/">(.*)</a></span>',html))

	return detail


def main():

	location = sys.argv[1]
	page_range = sys.argv[2]
	
	for start_index in range(0,int(page_range),25):
		html = getHtml("https://www.douban.com/group/beijingzufang/discussion?start="+str(start_index))
		lists = getInfo(html,location)
		for line in lists:
			result = re.search(r'<a href="(.*)" title="(.*)" class="">.*class="time">(.*)</td>',line)
			detail_lists = getDetail(result.group(1))
			article_id = result.group(1)[35:len(result.group(1))-1]
			print result.group(3),result.group(1),article_id,detail_lists[0][0],detail_lists[1][0],result.group(2)
            


if __name__ == '__main__':
	main()



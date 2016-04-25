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
        user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'] 
       
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','https://www.douban.com/group/topic/')]
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

	spider = BrowserBase()
	page = spider.openurl(url)
	html = page.read()
	detail = []
#	print html		
	pub_date = re.findall(r'<span class="color-green">(.*)</span>',html)
	if len(pub_date) == 0 :
		detail.append('0000-00-00 00:00:00')
	else:
		detail.append(pub_date[0])

	pub_user = re.findall(r'<span class="from">来自: <a href="https://www.douban.com/people/[a-zA-Z0-9_]+/">(.*)</a>.*</span>',html)
	if len(pub_user) == 0 :
		detail.append('无')
	else:
		detail.append(pub_user[0])

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
			print detail_lists[0],result.group(3),result.group(1),article_id,detail_lists[1],result.group(2)
            


if __name__ == '__main__':
	main()



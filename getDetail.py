#coding=utf-8

import urllib
import re
import sys


def getHtml(url):
    
    page = urllib.urlopen(url)
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
    

def main():

	page = urllib.urlopen("https://www.douban.com/group/topic/85595325/")
	html = page.read()
	#pub_info = re.findall(r'<a href=".*" title=".*'+location+'.*" class="">',html)	
  	print html


if __name__ == '__main__':
    main()

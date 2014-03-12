#!/usr/bin/env python
#$Id: wjmBlogger.py  08-04-2011 03:56PM William J. MacLeod(wimac1@gmail.com) ver: 11.220.2109
# file has title on first line and tags on second line and then content.

from gdata import service
import gdata
import atom
import sys
import getpass

def blogPoster():
    
    if len(sys.argv)==1:
        print 'Error: argument required.'
    else:
        file = sys.argv[1]

    post = open(file)
    user ='wimac1@gmail.com'
    #password = sys.argv[2] 
    password = getpass.getpass()

    # login
    blogger_service = service.GDataService(user,password)
    blogger_service.source = 'wjmBlogger-0.01'
    blogger_service.service = 'blogger'
    blogger_service.account_type = 'GOOGLE'
    blogger_service.server = 'www.blogger.com'
    blogger_service.ProgrammaticLogin()
    
    feed = blogger_service.Get('/feeds/default/blogs')    
    blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]


    entry = gdata.GDataEntry()
    entry.title = atom.Title('xhtml', text=post.readline())
    tags = post.readline().split(',')
    if tags == ['\n']:
        print 'no tags'
    else:
        for tag in tags :
            category = atom.Category(term=tag, scheme="http://www.blogger.com/atom/ns#")
            entry.category.append(category)
    entry.content = atom.Content(content_type='html', text=post.read()) 
    
    blogger_service.Post(entry, '/feeds/%s/posts/default' % blog_id)


    print('posted')
    post.close()

if __name__ == '__main__':
  blogPoster()

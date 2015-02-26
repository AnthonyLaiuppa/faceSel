#! Usr/bin/env python

from bs4 import BeautifulSoup

#data structor
"""
{

    "album_links": [{

    "name": "$NAME,

    "url": $URL,

    }],

}
"""
class Parser(object):

    def __init__(self):
        self.data = {}
        self.pictureData = {}

    def get_album_links(self):

        #get all links from soup
        album_div = self.soup.find_all("a", "photoTextTitle", True)
        # print album_div
        self.data['albums'] = []
        for a in album_div:
            url = a['href']
            name=a.find("strong").string
            output = {
                "name": name,
                "url": url,
            }

            self.data['albums'].append(output)
        return self.data['albums']

    def get_picture_links(self):

        #get all links from soup
        picture_div = self.soup.find_all("i", "uiThumbImg", True)
        #print picture_div
        self.pictureData['pictures'] = []
        for a in picture_div
            url = a['url']
            output ={
                "url": url,
            }

            self.pictureData['pictures'].append(output)
        return pictureData['pictures']


    def set_soup(self, html):
        self.soup = BeautifulSoup(html)


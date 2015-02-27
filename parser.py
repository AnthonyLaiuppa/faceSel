#! Usr/bin/env python

from bs4 import BeautifulSoup
import os, re, urllib, urllib2, simplejson
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
        self.data = {
            "albums": {},
        }
        self.picture_data = {}

    def get_album_links(self):

        #get all links from soup
        album_div = self.soup.find_all("a", "photoTextTitle", True)
        # print album_div
        for a in album_div:
            url = a['href']
            name = a.find("strong").string
            output = {
                "name": name,
                "url": url,
            }

            key = output['name'].replace(" ", "-")
            key = re.sub('[^A-Za-z0-9\-]+', '', key)

            self.data['albums'][key] = output
        return self.data['albums']

    def get_picture_links(self, album):
        if album not in self.data['albums'].keys():
            self.data['albums'][album] = {}

        #get all links from soup
        picture_div = self.soup.find_all("a", "uiMediaThumb", True)
        data = []
        for elem in picture_div:
            if 'ajaxify' in elem.attrs:
                href = urllib.unquote(elem['ajaxify'])
                src = re.search(r'src=(?P<src>.+)', str(href))
                if src != None:
                    output = {
                        "url": str(src.group(0)).replace("src=", "").split("&size")[0].split("&small")[0],
                        "ajaxify": href,
                    }

                    data.append(output)

        self.data['albums'][album]['pictures'] = data
        return data

    def get_data_json(self):
        return simplejson.dumps(self.json_convert(self.data), indent=2)

    def json_convert(self, data):
        if type(data) is dict:
            for i in data:
                data[i] = self.json_convert(data[i])
            return data
        elif type(data) is list:
            for idx, val in enumerate(data):
                data[idx] = self.json_convert(val)
            return data
        elif type(data) is str:
            return data.replace("'", "''")
        elif type(data) is unicode:
            return data
        else:
            return str(data)

    def set_soup(self, html):
        self.soup = BeautifulSoup(html)

    def create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_files(self):
        self.create_directory("data")
        self.data['fail'] = []
        for key, album in self.data['albums'].items():
            path = str("data/" + str(key))
            self.create_directory(path)
            count = 0
            for picture in album['pictures']:
                img_path = str(path + "/" + str(count) + ".jpg")
                image = urllib.URLopener()
                try:
                    image.retrieve(picture['url'], img_path)
                    count += 1
                except:
                    output = {
                        "album": key,
                        "picuture": picture
                    }
                    self.data['fail'].append(output)





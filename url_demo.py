import urllib.request as urllib2
import urllib.parse as urlparse
# -*- coding: UTF-8 -*-

data_auth = {
        'user_or_email': 'thinhlp',
        'password': '123456'
}

data_add = {
        'category_title': 'Test python edited 6',
        'category_parent': 0,
        'category_weight': 0,
        'category_alias': 'test-python-edited-6',
        'category_description': 'test python edited 6',
}

url_auth = 'http://core.me/admin/login'
url_category_add = 'http://core.me/admin/category/add'


def print_time(title, t):
        if t > 1:
                print ("%s: %s s" % (title, round(t,3)))
        else:
                timeload = round(t,4) * 1000
                print ("%s: %s ms" % (title, timeload))

# Create Session
data_auth_encode = urlparse.urlencode(data_auth).encode("utf-8")
req = urllib2.Request(url_auth)
resp = urllib2.urlopen(req, data=data_auth_encode)
cookie = resp.headers.get('Set-Cookie')

data_add_encode = urlparse.urlencode(data_add).encode("utf-8")
req2 = urllib2.Request(url_category_add)
req2.add_header('cookie', cookie)
resp2 = urllib2.urlopen(req2,data=data_add_encode)

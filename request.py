from requests import Request, Session

data_auth = {
        'user_or_email': 'thinhlp',
        'password': '123456'
}

data_add = {
        'category_title': 'Test python edited 1',
        'category_parent': 0,
        'category_weight': 0,
        'category_alias': 'test-python-edited',
        'category_description': 'test python edited',
}

data_article = {
	      'category_title': 'Test python edited 2',
        'category_parent': 0,
        'category_weight': 0,
        'category_alias': 'test-python-edited',
        'category_description': 'test python edited',
}

url_auth = 'http://core.me/admin/login'
url_category_add = 'http://core.me/admin/category/add'
url_article_add = 'http://core.me/admin/category/add'

def print_time(title, t):
        if t > 1:
                print ("%s: %s s" % (title, round(t,3)))
        else:
                timeload = round(t,4) * 1000
                print ("%s: %s ms" % (title, timeload))

# Create Session
s = Session()

post_auth = s.post(url_auth, data=data_auth)
time_auth = post_auth.elapsed.total_seconds()
print_time("Time auth", time_auth)

post_category = s.post(url_category_add, data=data_add)
time_post = post_category.elapsed.total_seconds()
print_time("Time Post", time_post)

post_article = s.post(url_article_add, data=data_article)
time_article = post_article.elapsed.total_seconds()
print_time("Category post", time_article)

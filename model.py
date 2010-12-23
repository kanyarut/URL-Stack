from google.appengine.ext import db
from google.appengine.ext import search

class Category(db.Model):
    account = db.UserProperty()
    name = db.StringProperty(multiline=False)

class Weblink(search.SearchableModel):
    unsearchable_properties = ['account', 'category', 'content','since','read', 'rating']
    account = db.UserProperty()
    category = db.StringProperty(multiline=False)
    url = db.StringProperty()
    tags = db.StringProperty()
    title = db.TextProperty()
    content = db.TextProperty()
    keyword = db.TextProperty()
    since = db.DateTimeProperty(auto_now_add=True)
    read = db.DateTimeProperty()
    rating = db.IntegerProperty()
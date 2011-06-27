import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import model
import parse
                
class List(webapp.RequestHandler):

    def get(self):
    	user = users.get_current_user()
        if user:
            beans = model.Weblink.all()
            
            beans.filter("account =", user)
            
            if self.request.get('c'):
            	beans.filter("category =", self.request.get('c'))
            	
            beans.filter("readlater =", 1)
            
            beans.order('-since')
            
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

            template_values = {
                'beans': beans,
                'url': url,
                'url_linktext': url_linktext,
            }
                
            path = os.path.join(os.path.dirname(__file__), 'template/m/list.html')
            self.response.out.write(template.render(path, template_values))
							
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Search(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            beans = model.Weblink.all().search(self.request.get('q')).filter("account =", user)
            template_values = {
                'beans': beans,
                'q': self.request.get('q'),
            }
            path = os.path.join(os.path.dirname(__file__), 'template/m/list.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Read(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('k'))
            q = db.GqlQuery("SELECT * FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            if(results[0].content == None):
                p = parse.Parse(results[0].url)
                results[0].content = p.getContent()
            
            if(results[0].read == None):
                results[0].read = 0
                
            template_values = {
                'hit': results[0].hit,
                'read': results[0].read,
                'title': results[0].title,
                'url': results[0].url,
                'key': k,
                'content': results[0].content,
            }
            
            results[0].read = 100
            results[0].save()
            
            path = os.path.join(os.path.dirname(__file__), 'template/m/read.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('key'))
            p = self.request.get('percent')
            q = db.GqlQuery("SELECT * FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            results[0].read = int(p)
            results[0].save()
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Visit(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('k'))
            q = db.GqlQuery("SELECT * FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            
            if(results[0].hit == None):
                results[0].hit = 0
            
            results[0].hit = results[0].hit+1
            results[0].save()
            
            self.redirect(results[0].url)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
application = webapp.WSGIApplication([  ('/m', List),
										('/m/search', Search),
										('/m/read', Read),
										('/m/visit', Visit)
										],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
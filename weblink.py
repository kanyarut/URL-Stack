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
            
            beans.order('-since')
            
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

            template_values = {
                'beans': beans,
                'url': url,
                'url_linktext': url_linktext,
            }
                
            path = os.path.join(os.path.dirname(__file__), 'template/list.html')
            self.response.out.write(template.render(path, template_values))
							
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Add(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            categories = db.GqlQuery("SELECT * FROM Category WHERE account = :1 ORDER BY name asc", user)
            template_values = {
                'categories': categories,
                'rel': self.request.get('rel'),
                'user': user,
            }
            path = os.path.join(os.path.dirname(__file__), 'template/addurl.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:
            url = self.request.get('url')
            q = db.GqlQuery("SELECT __key__ FROM Weblink WHERE account = :1 AND url = :2", user,url)
            results = q.fetch(1)
            if(len(results)<1):
                p = parse.Parse(url)
                if(p.error == 0):
                    bean = model.Weblink()
                    bean.account = user
                    bean.category = self.request.get('category')
                    bean.tags = self.request.get('tags')
                    bean.url = url
                    p = parse.Parse(url)
                    bean.title = p.getTitle()
                    bean.keyword = p.getKeyword()
                    bean.content = p.getContent()
                    bean.put()
                    template_values = {
                        'message': 'Added',
                    }
                    path = os.path.join(os.path.dirname(__file__), 'template/done.html')
                    self.response.out.write(template.render(path, template_values))	
                else:
                    self.redirect('/weblink/add?rel'+url)
            else:
                template_values = {
                    'message': 'Already Exist',
                }
                path = os.path.join(os.path.dirname(__file__), 'template/done.html')
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
            path = os.path.join(os.path.dirname(__file__), 'template/list.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Delete(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('k'))
            q = db.GqlQuery("SELECT __key__ FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            db.delete(results)
            self.redirect('/weblink')
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
            path = os.path.join(os.path.dirname(__file__), 'template/read.html')
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

class Edit(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('k'))
            q = db.GqlQuery("SELECT * FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            if(results[0].content == None):
                p = parse.Parse(results[0].url)
                results[0].content = p.getContent()
                results[0].save()
            
            categories = db.GqlQuery("SELECT * FROM Category WHERE account = :1 ORDER BY name asc", user)
            
            cate = []

            for category in categories:
                if(str(category.key()) == str(results[0].category)):
                    category.isselect=True
                else:
                    category.isselect=False
                cate.append(category)

            template_values = {
            	'categories': cate,
            	'bean':results[0],
            }
            path = os.path.join(os.path.dirname(__file__), 'template/edit.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self):
        user = users.get_current_user()
        if user:
            k = db.Key(self.request.get('key'))
            q = db.GqlQuery("SELECT * FROM Weblink WHERE account = :1 AND __key__ = :2", user,k)
            results = q.fetch(1)
            results[0].category = self.request.get('category')
            results[0].tags = self.request.get('tags')
            results[0].url = self.request.get('url')
            results[0].save()
            
            template_values = {
                'message': 'Done Editing',
            }
            path = os.path.join(os.path.dirname(__file__), 'template/done.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
application = webapp.WSGIApplication([  ('/weblink', List),
										('/weblink/add', Add),
										('/weblink/search', Search),
										('/weblink/delete', Delete),
										('/weblink/read', Read),
										('/weblink/edit', Edit),
										('/weblink/visit', Visit)
										],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
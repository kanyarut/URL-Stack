import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import model

class List(webapp.RequestHandler):
    def get(self):
    	user = users.get_current_user()

        if user:
            beans = db.GqlQuery("SELECT * FROM Category WHERE account = :1 ORDER BY name asc", user)
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
                'beans': beans,
                'url': url,
                'url_linktext': url_linktext,
            }

            path = os.path.join(os.path.dirname(__file__), 'template/category.html')
            self.response.out.write(template.render(path, template_values))
							
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Add(webapp.RequestHandler):
    def post(self):
    	user = users.get_current_user()
    
    	if user:
            bean = model.Category()
            bean.account = user
            bean.name = self.request.get('name')
            bean.put()
            self.redirect('/category')
							
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
application = webapp.WSGIApplication([('/category', List),('/category/add', Add)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
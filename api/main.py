import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class WarmUpPage(webapp2.RequestHandler):
    """
    This route is hit when a new instance is spinned up and it gives us a
    chance to prepare the state of the app, populate caches etc., before
    live traffic is directed to this instance.

    Must be exposed as `/_ah/warmup` GET route.

    Don't forget to enable `inbound_services: - warmup` in `app.yaml`
    Otherwise this will not work.
    """

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Everything that needs to be warmed up was.')


application = webapp2.WSGIApplication(
    [
        ('/_ah/warmup', WarmUpPage),
        ('/api/', MainPage)
    ],
    debug=True
)

import webapp2


def record_stats(app):
    """
    Wrapper for WSGI application (WSGI middleware).
    Enables stats collection for the app.

    The stats are normally exposed for admins on `/_ah/stats/` and require
    an `- appstats: on` entry in `app.yaml`

    :param app: WSGI application instance
    :return: same WSGI application instance wrapped into a stats recorder
    """
    from google.appengine.ext.appstats import recording
    return recording.appstats_wsgi_middleware(app)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


application = webapp2.WSGIApplication(
    [
        ('/', MainPage),
    ],
    debug=True
)

application = record_stats(application)

#!/usr/bin/env python

import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options



define("environment", default="development", help="Pick you environment", type=str)
define("site_title", default="Tornado Example", help="Site Title", type=str)
define("cookie_secret", default="sooooooosecret", help="Your secret cookie dough", type=str)
define("port", default=8000, help="Listening port", type=int)




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


class FourOhFourHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("404.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r"/", MainHandler),
           (r"/([^/]+)", FourOhFourHandler),
        ]
        settings = dict(
            site_title=options.site_title,
            cookie_secret=options.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    if "PORT" in os.environ:
        port = os.environ["PORT"]
    else:
        port = options.port
    print "Server listening on port " + str(port)
    tornado.options.parse_command_line()
    logging.getLogger().setLevel(logging.DEBUG)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

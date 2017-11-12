#coding:utf8

import tornado.ioloop
from app import Application
import tornado.httpserver
import config

if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(config.port)
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()



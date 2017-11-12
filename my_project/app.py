import tornado.web
from views.index import IndexHandler,UploadHandler,RegestHandler,LoginHandler
import config
import torndb
from tornado.web import url
from tornado.web import StaticFileHandler
import os

class Application(tornado.web.Application):
    def __init__(self):

        urls =[
            url(r'/',IndexHandler, name='index'),
            url(r'/upload',UploadHandler,name='upload'),
            (r'/upload/(.*)', StaticFileHandler, {'path': os.path.join(config.BASE_DIR, 'upload')}),
            url(r'/login',LoginHandler, name='login'),
            url(r'/regset',RegestHandler,name='login'),
        ]


        self.db = torndb.Connection(
            host="127.0.0.1",
            database="tornado_dome",
            user="root",
            password="111111",
        )
        
        super(Application, self).__init__(urls,**config.app_seting)


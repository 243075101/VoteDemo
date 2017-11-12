#coding:utf8

import tornado.web
import uuid
import config
import os
import hashlib


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        pass

    def upload_files(self,files,dbdir):
        message = ''
        is_ok = True
        dbname = None
        for file in files:
            content_type = file.get('content_type',None)
            if not (content_type == 'image/jpeg' or content_type =='image/png'):
                self.write(message)
                is_ok = False
                message = '文件类型不正确'

        if is_ok:
            for file in files:
                dirname = self.make_dir(dbdir)
                filename = file.get('filename',None)
                body = file.get('body',None)
                dbname = str(uuid.uuid4())+'.'+filename.split('.')[-1]
                fname = dirname + '/'+dbname

                with open(fname,'wb') as f:
                    f.write(body)
            message = 'upload is ok'

        return is_ok,message,dbname


    def make_dir(self,dbdir):
        dirname = os.path.join(config.BASE_DIR, 'upload/' + dbdir)
        if not os.path.exists(dirname):  # 文件夹不存在
            os.makedirs(dirname)
        return dirname

    def encrypt(self, str):
        ept = hashlib.sha1(str)
        str = ept.hexdigest()
        return str
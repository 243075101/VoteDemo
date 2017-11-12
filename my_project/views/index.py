#coding:utf8
from lib.baseHandler import BaseHandler
import datetime
import uuid

session_info = {
    # 'sllsdjflkjslkdflk' : {'username':'alice','user_level':3},
    # 'sllsdfsffsdfkdflk' : {'username':'alice','user_level':3}
}

class Session(object):
    def __init__(self ,handler):
        self.handler = handler
        self.session_id = None
    # 添加一条session
    def set_value(self,key,value):
        # 1.在服务端生成随机字符串,写入session字典，
        # 2.在字典里添加键值对
        # 3.在客户端写入session_id
        if self.session_id is None:
            session_id = self.handler.get_cookie('session_id',None)
            if session_id is None: # 浏览器端没有session_id
                session_id = self.__get_session_id()
                session_info[session_id] = {}
            else:# 浏览器端有session_id

                if session_id not in session_info: # 服务器端没有相应的session_id
                    session_id = self.__get_session_id()
                    session_info[session_id] = {}
                else:
                    pass
            self.session_id = session_id
        session_info[self.session_id][key] = value
        self.handler.set_cookie('session_id',self.session_id)

    # 获取一个session
    def get_value(self,key):
        value = None
        session_id = self.handler.get_cookie('session_id',None)
        if session_id is None: # 客户端浏览器不存在session_id
            return value

        user_info = session_info.get(session_id,None)
        if user_info is None: # 服务端没有session_id
            return value

        value = user_info.get(key,None) # 返回响应value
        return value

    # 获取一个session_id
    def __get_session_id(self):
        session_id = str(uuid.uuid4())
        return session_id

class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.set_header("X-XSS-Protection", 0)
        sql = 'select * from goods'
        res = self.application.db.query(sql)
        print res

        #self.write({'res':res})

        self.render('index.html', files=res)




class UploadHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.set_header("X-XSS-Protection", 0)  # Ghrome 浏览览器加
        self.render('upload.html')

    def post(self, *args, **kwargs):

        name = self.get_body_argument('name',None)
        age = self.get_body_argument('age',None)
        score = self.get_body_argument('score', None)
        price = self.get_body_argument('price', None)
        files = self.request.files.get('pic',None)

        is_ok,message,dbname = self.upload_files(files,'goods_pic')
        if is_ok:

            if dbname is not None:
                dbname = '/goods_pic/'+dbname
            else:
                dbname = 'default.jpg'

            now = datetime.datetime.now().strftime('%H-%m-%d %H:%M:%S')

            sql = 'insert into goods(name,price,age,pic,score,date_add) values("%s",%.2f,"%d","%s","%ld","%s")' % (
                name,
                float(int(price)),
                int(age),
                dbname,
                int(score),
                now,
            )
            print sql
            try:
                self.application.db.execute(sql)  # 执行sql 语句
                self.redirect('/')
            except Exception, e:
                print str(e)
        else:
            self.write(message)

class RegestHandler(BaseHandler):

     def get(self, *args, **kwargs):
         self.render('regest.html')

     def post(self, *args, **kwargs):

         username = self.get_body_argument('username')
         password = self.get_body_argument('password')

         password = self.encrypt(password)

         now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

         sql = 'insert into user(username,password,level,date_add) values("%s","%s","%s","%s")' %(
             username,
             password,
             '0',
             now
         )
         try:
            self.application.db.execute(sql)

            self.redirect('login')
         except Exception,e:
             print e


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):

        self.render('login.html')

    def post(self, *args, **kwargs):

        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        if username and password:  # 都不为空
            password = self.encrypt(password)  # 给密码加密

            # 用户查询语句
            sql = 'select * from user where username="%s" and password="%s"' % (username, password)
            res = self.application.db.query(sql)  # 返回结果集 []
            if len(res) == 1:  # 查到用户了 ,登陆成功

                to_url = self.reverse_url('index')
                self.redirect(to_url)  # 跳转
            else:
                self.write('用户名密码不正确 fuck off')
        else:
            self.write('用户名或密码不能为空')


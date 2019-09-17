'''
httpserver 2.0
env: python3.6
io多路复用 http练习
'''
from socket import *
from select import select




class HTTPServer:

    def __init__(self,host = '0.0.0.0',port = 80,dir = None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host,port)
        #select 监控列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()
    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)

    def serve_forever(self):
        self.sockfd.listen(3)
        print('Listen the port %d'%self.port)
        # 设置关注IO
        self.rlist.append(self.sockfd)
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c,addr = r.accept()
                    self.rlist.append(c)

                else:
                    # 有客户端发请求
                    self.handle(r)

    def handle(self,confd):
        #接收请求
        request = confd.recv(4096)
        # 客户端断开处理
        if not request:
            self.rlist.remove(confd)
            confd.close()
            return
        # 提取请求内容

        request_line = request.splitlines()[0]
        info = request_line.decode().split(' ')[1]
        print(info)

        # 根据info情况分类
        if info == '/' or info[-5:] == '.html':
            self.get_html(confd,info)
        else:
            self.get_data(confd ,info)

    def get_html(self,confd,info):

        if info == '/':
             # 主页
            filename = self.dir+'/index.html'
        else:
             # 其他网页
            filename =self.dir+info
            try:
                f = open(filename)
            except Exception:
                # 没有网页
                response = 'HTTP/1.1 404 Not Found\r\n'
                response += 'Content-Type:text/html\r\n'
                response += '\r\n'
                response += '<h1>sorry</h1>'
            else:
                # 有网页
                response = 'HTTP/1.1 200 OK\r\n'
                response += 'Content-Type:text/html\r\n'
                response += '\r\n'
                response += f.read()

    def get_data(self,confd,info):
        f = open(self.dir+'/timg.jpeg','rb')
        response ='HTTP/1.1 200 OK\r\n'
        response += 'Content-Type:image/jpeg\r\n'
        response += '\r\n'
        response = response.encode()+f.read()
        confd.send(response)




if __name__ == '__main__':
    # 用户自己提供的内容
    HOST = '0.0.0.0'
    PORT = 8888
    DIR = "./static" # 网页目录

    http = HTTPServer(HOST,PORT,DIR) # 实例化对象
    http.serve_forever() #启动服务
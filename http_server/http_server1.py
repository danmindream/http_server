from socket import *
def handle(connfd):
    data=connfd.recv(4096).decode()
    request_line = data.split('\n')[0]
    info = request_line.split(' ')[1]
    if info== '/':
        with open('index.html') as f:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += f.read()
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Sorry...<h1>"
    connfd.send(response.encode())



def main():
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('127.0.0.1',8888))
    s.listen(8)
    while True:
        connfd,addr = s.accept()
        print('Connect from',addr)
        handle(connfd)


main()



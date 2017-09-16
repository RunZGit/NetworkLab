#!/usr/bin/python

from abc import ABCMeta, abstractmethod
import socket, sys, time, os, stat

DEFAULT_HOST = '127.0.0.1'
DEFAULT_CONNECTIONS = 5
DEFAULT_FILE_LOCATIONS = './Upload'
DEFAULT_VERSION = "HTTP/1.0"

class Response(object):
    def __init__(self, version="HTTP/1.0", status=200, message='OK'):
        self.status = status
        self.message = message
        self.version = version
        self.config = {}
        self.body = ""

    def addConfigs(key, value):
        self.config[key] = value

    def __str__(self):
        response =  "{0} {1} {2}\r\n".format(self.version, self.status, self.message)
        for key in self.config:
            response+= "{0}: {1}\r\n"
        response+="\n" + self.body
        return response


class Builder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_version(self, value):
        pass

    @abstractmethod
    def set_status(self, value):
        pass

    @abstractmethod
    def set_message(self, value):
        pass

    @abstractmethod
    def set_body(self, value):
        pass

    @abstractmethod
    def add_config(self, key, value):
        pass

    @abstractmethod
    def get_result(self):
        pass


class ResponseBuilder(Builder):
    def __init__(self):
        self.response = Response()

    def set_version(self, value):
        self.response.version = value

    def set_status(self, value):
        self.response.status = value

    def set_message(self, value):
        self.response.message = value

    def set_body(self, value):
        self.response.body = value

    def add_config(self, key, value):
        self.response.config[key] = value

    def get_result(self):
        return self.response


# class ResponseBuilderDirector(object):
#     @staticmethod
#     def construct(request):

#         builder = ResponseBuilder()
#         builder.set_status(status)
#         builder.set_message(message)

#         return builder.get_result()



class RequestHandler(object):
    def __init__(self, cSocket, default_buffer_size = 1024):
        self.cSocket = cSocket
        self.default_buffer_size = default_buffer_size

    def handleRequest(self):
        (requestType, filePath) = self.parseRequest()
        response = self.buildResponce(requestType, filePath)
        self.cSocket.sendall(str(response))
        del response
        self.cSocket.close()

    def buildResponce(self, requestType, filePath):
        builder = ResponseBuilder()
        builder.set_version(DEFAULT_VERSION)

        if requestType in ['GET', 'HEAD']:
            if not self.hasFile(filePath):
                builder.set_status('404')
                builder.set_message('Not Found')
            elif not self.hasPermissionToRead(filePath):
                builder.set_status('403')
                builder.set_message('Forbidden')
            else:
                fileType = filePath[(filePath.rfind('.')+1):]
                if fileType == "html":
                        builder.add_config("Content-Type", "text/html")
                elif fileType in ['jpg', 'jpeg', 'png']:
                    builder.add_config("Content-Type", "image/gif")

                content = self.loadFile(filePath)
                builder.add_config("Last-Modified", time.ctime(os.path.getmtime(filePath)))
                builder.add_config("Content-Length", str(len(content)))
                
                if requestType == 'GET':
                    builder.set_status('200')
                    builder.set_message('OK')
                    builder.set_body(content)
                else:
                    builder.set_status('302')
                    builder.set_message('FOUND')
                del content
        else:
            builder.set_status('501')
            builder.set_message('Not Implemented')

        return builder.get_result()

    def parseRequest(self):
        request = self.cSocket.recv(self.default_buffer_size)
        request = request.splitlines()[0]
        request = request.rstrip('\r\n')
        (requestType, filePath, _) = request.split()
        if filePath == "/":
            filePath = "/index.html"
        filePath = DEFAULT_FILE_LOCATIONS+filePath
        return (requestType, filePath)

    def hasPermissionToRead(self, filePath):
        # Make sure checks file exists before read
        st = os.stat(filePath)
        return bool(st.st_mode & stat.S_IRWXO)

    def hasFile(self, filePath):
        return os.path.exists(filePath)

    def loadFile(self,filePath):
        with open(filePath, 'r') as f:
            content = f.read()
        return content


def main(port):
    # Before run multithread! Learn how to kill it first!
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((DEFAULT_HOST, port))
    serversocket.listen(DEFAULT_CONNECTIONS)

    while True:
        try:
            (cSocket, address) = serversocket.accept()
            # ct = client_thread(cSocket)
            # ct.run()
            requestHandler = RequestHandler(cSocket)
            requestHandler.handleRequest()
        except KeyboardInterrupt:
            print '\rBye bye!\n'
            serversocket.close()
            sys.exit()



if __name__ =='__main__':
    args = sys.argv[1:]
    if not len(args) == 1 or not args[0].isdigit():
        print 'Command not supported. \nExample: python server.py 1234\n'
        sys.exit()
    main(int(args[0]))















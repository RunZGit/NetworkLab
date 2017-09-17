# Programming Assignment 1 Web Server

## Assumptions:

Required: python2.7
HTTP standard: 1.0   

### Server
All the files are stored in the ./Upload directory. 
Only GET and HEAD methods are supported. 
By default, debug mode is off. Once it is on, the server will run on localhost instead of the socket.getHostName(). 
The server is designed using builder pattern, which you can reference from [Wikipedia](https://en.wikipedia.org/wiki/Builder_pattern).
To stop the server, type ctrl+c.

### Client
All the files are downloaded in the ./Download folder
Client only supports GET and HEAD methods. 
If GET method succeed, it will only store the body of the response.
Else and other methods will store the entire response to the download folder under the request name.
By default, the client will only throw error message 'Your input has problems!'. If you believe that is not the case, please remove the try catch clause surronding the main(args) call.


## Commands for server.py
```bash
./server.py [port] [debug_mode=False]
# Or
python server.py [port] [debug_mode=False]
```

## Commands for client.py
```bash
./client.py [host] [port] [file_location] [Method=GET/HEAD]
# Or
python client.py [host] [port] [file_location] [Method=GET/HEAD]
```
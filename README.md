# log monitoring
Monitoring server log file from browser.  The idea is to feed log fail to client application in the same manner as "tail -f".  The client application can be any application connecting to the server using websocket.  The client application does not need refresh.
## Server
The broadcast_tail_file.py will register the client applications feed the new content to the clients.
### Usage
python broadcast_tail_file.py [log file] [port]
### Prerequisites
python 3.7 or above \
websockets
## html
This html serve as a sample client application of how to connect to the server to receive log feed.  It's ready to use though.

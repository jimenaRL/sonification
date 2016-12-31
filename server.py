import os, sys
import types
import numpy as np


from OSC import OSCServer, OSCMessage, getUrlStr

def handle_timeout(self):
    """ this method of reporting timeouts only works by convention
        that before calling handle_request() field .timed_out is
        set to False
    """
    self.timed_out = True

def woman_callback(path, tags, args, source):

    indent = np.random.randint(0,10)
    out = "\t" * indent
    out += " ".join([str(arg) for arg in args])
    out += "\n"
    print out
    return

def quit_callback(path, tags, args, source):
    global run
    run = False

# create server
HOST = "localhost"
PORT = 9001
server = OSCServer((HOST,PORT))
server.timeout = 0
run = True
# print "Running | ip addresse : %s | port : %s" % (HOST,PORT)

print ("\n"*100)
print ("gender data sonification "*997)

# add handle_timeout method to the server
server.handle_timeout = types.MethodType(handle_timeout, server)

# add callback methods to the server
server.addMsgHandler( "/woman", woman_callback)
server.addMsgHandler( "/quit", quit_callback )


# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

while run:
    each_frame()

server.close()
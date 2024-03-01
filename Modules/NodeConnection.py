from p2pnetwork.nodeconnection import NodeConnection

class MyNodeConnection (NodeConnection):
    # Python class constructor
     def __init__(self, main_node, sock, id, host, port):
        super(MyNodeConnection, self).__init__(main_node, sock, id, host, port)

    # Check yourself what you would like to change and override! See the 
    # documentation and code of the nodeconnection class.
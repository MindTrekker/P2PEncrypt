import os.path
from p2pnetwork.node import Node
from Modules import OurSha256
class MyNode (Node):
    

    def __init__(self, host, port, id=None, callback=None, max_connections=0, debug=False):
        super(MyNode, self).__init__(host, port, id, callback, max_connections)
        print("MyNode: Start")

    @property
    def Connections(self):
        return self.connections

    def outbound_node_connected(self, node):
        if (self.debug):
            print("outbound_node_connected (" + self.id + "): " + node.id)
        else:
            print("\nConnection Sucessfull...")
            
    def inbound_node_connected(self, node):
        if (self.debug):
            print("inbound_node_connected: (" + self.id + "): " + node.id)
        else:
            print("\nRemote Node Connected...")

    def inbound_node_disconnected(self, node):
        if (self.debug):
            print("inbound_node_disconnected: (" + self.id + "): " + node.id)
        else:
            print("\nRemote Node Disconnected...")

    def outbound_node_disconnected(self, node):
        if (self.debug):
            print("outbound_node_disconnected: (" + self.id + "): " + node.id)
        else:
            print("\nConnection Terminated...")

    def node_message(self, node, data):
        if (self.debug):
            print("node_message (" + self.id + ") from " + node.id + ": " + str(data))
        else:
            newdata = str(data).removeprefix("¶")
            if (str(data) != newdata):
                splitData = newdata.lower().split(",")
                if not os.path.exists("contact" + splitData[0] + ".txt"):
                    f = open("contact" + splitData[0] + ".txt", 'w')
                    f.write(newdata)
                    f.close
            else:
                hash = data[-64:]
                data = data[:-64]
                if hash == OurSha256.Hash256(data):
                    print(">> Hash " + hash + " is correct.")
                print("->" + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        if (self.debug):
            print("node wants to disconnect with other outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        if (self.debug):
            print("node is requested to stop (" + self.id + "): ")
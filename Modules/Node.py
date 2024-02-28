from p2pnetwork.node import Node
class MyNode (Node):
    def __init__(self, host, port, id=None, callback=None, max_connections=0, debug=False):
        super(MyNode, self).__init__(host, port, id, callback, max_connections)
        print("MyNode: Start")

    def outbound_node_connected(self, node):
        if (self.debug):
            print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        if (self.debug):
            print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        if (self.debug):
            print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        if (self.debug):
            print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        if (self.debug):
            print("node_message (" + self.id + ") from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        if (self.debug):
            print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        if (self.debug):
            print("node is requested to stop (" + self.id + "): ")
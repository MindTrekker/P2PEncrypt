import os.path
from p2pnetwork.node import Node
from Modules import OurSha256
import Modules.OurECEIS as OurECEIS
import Modules.generate_points as ECC
import Modules.ECEIS as ECEIS
from ast import literal_eval
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
            order, point, a, p = ECC.shared_point_generator()
            remotePubKey = ()
            privKey = 0
            remoteUser = ""
            newdata = str(data).removeprefix("¶")
            if (str(data) != newdata):
                splitData = newdata.lower().split(";")
                if not os.path.exists("contact" + splitData[0] + ".txt"):
                    f = open("contact" + splitData[0] + ".txt", 'w')
                    f.write(newdata)
                    f.close
                remoteUser = splitData[0]
                nf = open("remoteUser.txt", 'w')
                nf.write(remoteUser)
                nf.close
            else:
                #decrypt and such
                ##get our private key
                curUser = ""
                if os.path.exists("currentUser.txt"):
                    f = open("currentUser.txt", 'r')
                    curUser = f.readline()
                    f.close
                if os.path.exists("remoteUser.txt"):
                    f = open("remoteUser.txt", 'r')
                    remoteUser = f.readline()
                    f.close
                if os.path.exists("contact" + remoteUser + ".txt"):
                    f = open("contact" + remoteUser + ".txt", 'r')
                    remotePubKey = literal_eval(f.readline().split(";")[3])
                    f.close
                if os.path.exists("private" + curUser + ".txt"):
                    f = open("private" + curUser + ".txt", 'r')
                    privKey = int(f.readline().split(";")[1])
                    f.close
                ##decrypt
                sharedKey = ECC.calc_shared_point(privKey,remotePubKey, a, p)
                cypherTagNonnce = data.split("¶")
                data = OurECEIS.eceis_decrypt(str(sharedKey), bytes.fromhex(cypherTagNonnce[0]), bytes.fromhex(cypherTagNonnce[1]),bytes.fromhex(cypherTagNonnce[2]))
                ##hash
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
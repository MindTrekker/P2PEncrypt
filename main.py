import sys
import os.path
sys.path.insert(0, r'..\Modules') # Import the files where the modules are located

from Modules.Node import MyNode
from Modules.NodeConnection import MyNodeConnection

# The port to listen for incoming node connections
publicDefaultKey = 1234567890
testIP = "127.0.0.1"
port = 9876 # default

# Syntax file_sharing_node.py port
if len(sys.argv) > 1:
    port = int(sys.argv[1])

#create default file
if not os.path.exists("default.txt"):
    f = open("default.txt",'w')
    f.write("default," + testIP + "," + str(port) + "," + str(publicDefaultKey))
    f.close()

curUser = input("> Local User Name:")
conInfo = ""
while conInfo == "":
    if os.path.exists(curUser.lower() + ".txt"):
        fi = open(curUser.lower() + ".txt", 'r')
        conInfo = fi.readline()
        fi.close()
    else:
        print("user file does not exist")
        
# Instantiate the node MyNode, it creates a thread to handle all functionality
node = MyNode(testIP, port,None,None,1)

# Start the node, if not started it shall not handle any requests!
node.start()

# The method prints the help commands text to the console
def print_help():
    print("?stop - Stops the application.")
    print("?help - Prints this help text.")
    print("?connect - Connect to  a remote node. Args are Host and Port.")
    print("?disconnect - Disonnect from the current node.")
    print("?cinfo - Get connection info.")

def node_connect(node:MyNode):
    
    ipIn = input("> Remote Host:")
    if (ipIn[0].isalpha()):
        #name stuff
        if os.path.exists(ipIn.lower() + ".txt"):
            fo = open(ipIn.lower() + ".txt",'r')
            info = fo.readline()
            fo.close()
            splitInfo = info.split(",")
            foIP = splitInfo[1]
            foPort = int(splitInfo[2])
            node.connect_with_node(foIP, foPort)
    else:
        portIn = int(input("> Remote Port:"))
        node.connect_with_node(ipIn, portIn)
    
    node.send_to_nodes("¶" + conInfo)

# Implement a console application
def Inputs():
    
    print("Connect to a remote node to get started: type?help for a list of commands")
    connected = False
    command = input()
    while ( command != "?stop" ):
            
            if len(node.all_nodes) >= 1:
                connected = True
            else:
                connected = False

            if ( command == "?help" ):
                print_help()

            elif ( command == "?connect" ):
                node_connect(node)
    
            elif (command == "?cinfo"):
                node.print_connections()

            elif ( command == "?disconnect" ):
                if (len(node.nodes_outbound) > 0):
                    node.disconnect_with_node(node.nodes_outbound[0])
                if (len(node.nodes_inbound) > 0):    
                    node.disconnect_with_node(node.nodes_inbound[0])
            else:
                if connected:
                    node.send_to_nodes(command)
                else:
                    print("No nodes Connected.")

            command = input()

Inputs()
node.stop()

#node.connect_with_node('127.0.0.1', port)
#node.send_to_nodes("message")
#node.start()
#node.stop()
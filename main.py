import sys
import time
sys.path.insert(0, r'..\Modules') # Import the files where the modules are located

from Modules.Node import MyNode
from Modules.NodeConnection import MyNodeConnection

# The port to listen for incoming node connections
port = 9876 # default

# Syntax file_sharing_node.py port
if len(sys.argv) > 1:
    port = int(sys.argv[1])

# Instantiate the node MyNode, it creates a thread to handle all functionality
node = MyNode("127.0.0.1", port,None,None,1)

# Start the node, if not started it shall not handle any requests!
node.start()

# The method prints the help commands text to the console
def print_help():
    print("stop - Stops the application.")
    print("help - Prints this help text.")
    print("connect - Connect to  a remote node. Args are IP address and Port.")

def node_connect(node:MyNode):
    ipIn = input("> IP Address:")
    portIn = int(input("> Port:"))
    node.connect_with_node(ipIn, portIn)

'''
def write_to(node:MyNode):
    inText = ""
    print("Messaging open. Type \"$exit\" to return to the menu")
    while (inText != "$exit"):
        inText = input(">")
        node.send_to_nodes(inText)
'''
# Implement a console application
connected = False
prompt = "? "
command = input(prompt)
while ( command != "stop" ):
    if ( command == "help" ):
        print_help()

    elif ( command == "connect" ):
        node_connect(node)
    
    elif (command == "cinfo"):
        node.print_connections()

    elif ( command == "write" ):
        if connected:
            inText = input("> ")
            node.send_to_nodes(inText)
        else:
            print("No nodes Connected.")

    else:
        print( command + " is not a command.")

    if len(node.all_nodes) >= 1:
        connected = True

    if connected:
        prompt = "! "
    else:
        prompt = "? "
    command = input(prompt)

node.stop()

#node.connect_with_node('127.0.0.1', port)
#node.send_to_nodes("message")
#node.start()
#node.stop()
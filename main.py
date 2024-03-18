import sys
import os.path
sys.path.insert(0, r'..\Modules') # Import the files where the modules are located

from Modules.Node import MyNode
from Modules.NodeConnection import MyNodeConnection
from ast import literal_eval
import Modules.OurSha256 as OurSha256
import Modules.OurECEIS as OurECEIS
import Modules.generate_points as ECC
import Modules.ECEIS as ECEIS


from hashlib import sha256

# The port to listen for incoming node connections
publicDefaultKey = 1234567890
testIP = "127.0.0.1"
port = 9876 # default

#hardcoded vales
order, point, a, p = ECC.shared_point_generator()

# Syntax file_sharing_node.py port
if len(sys.argv) > 1:
    port = int(sys.argv[1])

#create default file
if not os.path.exists("default.txt"):
    f = open("default.txt",'w')
    f.write("default," + testIP + ";" + str(port) + ";" + str(publicDefaultKey))
    f.close()

curUser = ""
conInfo = ""
while conInfo == "":
    curUser = input("> Local User Name:")
    if os.path.exists(curUser.lower() + ".txt"):
        fi = open(curUser.lower() + ".txt", 'r')
        conInfo = fi.readline()
        splitinfo = conInfo.split(";")
        testIP = splitinfo[1]
        port = int(splitinfo[2])
        fi.close()
    else:
        print("User file does not exist...")

    nfi = open("currentUser.txt", 'w')
    nfi.write(curUser)
    nfi.close()
        
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
    print("?adduser - creates a new user file.")
    print("?changekeys - debug method to alter stored keys.")

def node_connect(node:MyNode):
    ipIn = input("> Remote Host:")
    if (ipIn[0].isalpha()):
        #name stuff
        if os.path.exists("contact" + ipIn.lower() + ".txt"):
            fo = open("contact" + ipIn.lower() + ".txt",'r')
            info = fo.readline()
            fo.close()
            splitInfo = info.split(";")
            foIP = splitInfo[1]
            foPort = int(splitInfo[2])
            node.connect_with_node(foIP, foPort)
        else:
            print("Contact not found...")
    else:
        portIn = int(input("> Remote Port:"))
        node.connect_with_node(ipIn, portIn)
    
    node.send_to_nodes("¶" + conInfo)
    return ipIn

def create_user(name:str,host:str = testIP, uport:str = str(port)):
    #random key generator code here
    privatekey = ECC.create_private_key(order)
    publickey = ECC.create_public_key(point, privatekey, a, p)
    if not os.path.exists(name.lower() + ".txt"):
            naf = open(name.lower() + ".txt",'w')
            naf.write(name + ";" + host + ";" + str(uport) + ";" + str(publickey))
            naf.close()
    else:
        print("User Already Exists...")
    if not os.path.exists("private" + name.lower() + ".txt"):
            naf = open("private" + name.lower() + ".txt",'w')
            naf.write(name + ";" + str(privatekey))
            naf.close()
def getPubKey(remote:str):
     if os.path.exists("contact" + remote.lower() + ".txt"):
            fo = open("contact" + remote.lower() + ".txt",'r')
            info = fo.readline()
            fo.close()
            splitInfo = info.split(";")
            return literal_eval(splitInfo[3])
# Implement a console application
def Inputs():
    privKey = 0
    remotePubKey = ()
    remoteHost = ""
    if os.path.exists("private" + curUser.lower() + ".txt"):
            fo = open("private" + curUser.lower() + ".txt",'r')
            info = fo.readline()
            fo.close()
            privKey = int(info.split(";")[1])
    
    print("Connect to a remote node to get started: type?help for a list of commands")
    connected = False
    command = input()
    while ( command != "?stop" ):
        if (command != ""):
            if len(node.all_nodes) >= 1:
                connected = True
            else:
                connected = False

            if (command[0] == "?"):
                if ( command == "?help" ):
                    print_help()

                elif ( command == "?connect" ):
                    remoteHost = node_connect(node)
                    nf = open("remoteUser.txt", 'w')
                    nf.write(remoteHost)
                    nf.close
                    
                elif ( command == "?cinfo" ):
                    node.print_connections()

                elif ( command == "?disconnect" ):
                    if (len(node.nodes_outbound) > 0):
                        node.disconnect_with_node(node.nodes_outbound[0])
                    if (len(node.nodes_inbound) > 0):    
                        node.disconnect_with_node(node.nodes_inbound[0])

                elif ( command == "?adduser" ):
                    uname = input("> Username: ")
                    uhost = input("> User Host: ")
                    uport = input("> User Port: ")
                    create_user(uname,uhost,uport)
                #elif ( command == "?changeKeys" ):
                    #unipmlimented
                else:
                    print(command + "is not a Valid Command.")
            else:
                if connected:
                    #hash call
                    print("LibHash: " + sha256(command.encode('utf-8')).hexdigest())
                    hash = OurSha256.Hash256(command)
                    print("OurHash: " + hash)
                    #append hash to message
                    command = command + hash
                    #encrypt method call
                    nf = open("remoteUser.txt", 'r')
                    remoteHost = nf.readline()
                    nf.close
                    #print("ECEIS cyphertext:" + ECEIS.lib_ECEIS_encrypt(command))
                    remotePubKey = getPubKey(remoteHost)
                    key = OurECEIS.our_ecdh(privKey, remotePubKey, a, p)
                    cyphertext, tag, nonnce = OurECEIS.eceis_encrypt(command, key)
                    print("OurECEIS cyphertext: " + cyphertext.hex())
                    node.send_to_nodes(cyphertext.hex() + "¶" + tag.hex() + "¶" + nonnce.hex())
                else:
                    print("No nodes Connected.")

        command = input()

Inputs()
node.stop()

#node.connect_with_node('127.0.0.1', port)
#node.send_to_nodes("message")
#node.start()
#node.stop()
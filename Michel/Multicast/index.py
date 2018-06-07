#importacao de bibbliotcas
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
from MulticastController import MulticastController

log = core.getLogger()
multicastController = MulticastController("0.0.0.0.0", "00:00:00:00:00:00", 80)

def matchMulticastRequest (event):
    
    msg = of.ofp_flow_mod()
    if (of.ofp_match(
        nw_dst = IPAddr(multicastController.getServerIPAddress()),
        dl_dst = EthAddr(multicastController.getServerMAC()),
        in_port = multicastController.getServerPort()
    )):
        multicastController.addMember(event.parsed.next.srcip)

def matchMulticastContent (event):
    return None

def _handle_PacketIn (event):

    matchMulticastRequest(event)
    matchMulticastContent(event)

def launch ():

    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Grupo multicast iniciado")



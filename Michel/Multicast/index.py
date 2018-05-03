#importacao de bibbliotcas
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
from MulticastController import MulticastController

log = core.getLogger()
multicastController = MulticastController("0.0.0.0.0", "00:00:00:00:00:00:00:00", 80)

def matchMulticastRequest ():
    
    msg = of.ofp_flow_mod()
    match = of.ofp_match(
        nw_dst = IPAddr(multicastController.getServerIPAddress()),
        dl_dst = EthAddr(multicastController.getServerMAC()),
        in_port = multicastController.getServerPort()
    )



def matchMulticastContent ():
    return None

def _handle_ConnectionUp (event):

    matchMulticastRequest()
    matchMulticastContent()

def launch ():

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Grupo multicast iniciado")



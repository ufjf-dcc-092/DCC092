#importacao de bibbliotcas
import networkx as nx
from Node import Node
from Edge import Edge
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.host_tracker import host_tracker
from pox.openflow.discovery import Discovery  
from pox.lib.addresses import IPAddr, EthAddr
from MulticastController import MulticastController

log = core.getLogger()
networkTopology = nx.Graph()
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

def _handle_LinkEvent (event):
    l = event.link
    #criar nós do tipo isHost=false se eles não existem
    link1 = Node(l.dpid1, false)
    link2 = Node(l.dpid2, false)

    if( not link1 in networkTopology):
        networkTopology.add_node(link1)
        log.info("switch " + link1.id + " adicionado ao grafo de topologia")
    if( not link2 in networkTopology):
        networkTopology.add_node(link2)
        log.info("switch " + link2.id + " adicionado ao grafo de topologia")
    #criar aresta com weight 1
    edge = Edge(link1, link2, l.port1, l.port2, 1)
    if (not edge in networkTopology):
        networkTopology.add_edge(link1, link2, object = edge)
        log.info("switch " + link1.id + " conectado ao switch " + link2.id + " nas portas " + link1.port + " e " + link2.port + " respectivamente")

def _handle_HostEvent (event):

def launch ():
    
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)
    core.host_tracker.addListenerByName("HostEvent", _handle_HostEvent)
    log.info("controlador iniciado")



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
multicastController = MulticastController()

def matchMulticastRequest (event):
    
    msg = of.ofp_flow_mod()
    channelIP = str(msg.match.nw_dst)
    source = str(msg.match.dl_src)
    
    if multicastController.hasChannel(channelIP):

        for member in multicastController.getMembers(channelIP):
            path = nx.dijkstra_path(networkTopology, source, member, "weight")
            
            for x in range(len(path) - 1):
                msg.actions.append(of.ofp_action_output( port = networkTopology[ path[x] ][ path[x + 1] ]["object"].port1) )
                connection = core.openflow.getConnection( path[ x ].id )
                connection.send(msg)
                networkTopology[ path[x] ][ path[x + 1] ]["weight"] = 0

def _handle_PacketIn (event):
    matchMulticastRequest(event)

def _handle_LinkEvent (event):
    l = event.link
    #criar nos do tipo isHost=false se eles não existem
    link1 = Node(str(l.dpid1), False)
    link2 = Node(str(l.dpid2), False)

    if( not link1 in networkTopology):
        networkTopology.add_node(link1)
        log.info("switch " + link1.id + " adicionado ao grafo de topologia")
    if( not link2 in networkTopology):
        networkTopology.add_node(link2)
        log.info("switch " + link2.id + " adicionado ao grafo de topologia")
    #criar aresta com weight 1
    edge = Edge(l.dpid1, l.dpid2, str(l.port1), str(l.port2))
    if (not edge in networkTopology):
        networkTopology.add_edge(link1, link2, object = edge, weight = 1)
        log.info("switch " + link1.id + " conectado ao switch " + link2.id + " nas portas " + edge.port1 + " e " + edge.port2 + " respectivamente")

def _handle_HostEvent (event):
    #even.entry.macaddr,event.entry.dpid, event.entry.port
    host = Node(str(event.entry.macaddr), True)
    link = Node(str(event.entry.dpid), False)
    edge = Edge(event.entry.dpid, event.entry.macaddr, str(event.entry.port), None)
    if(not host in networkTopology and networkTopology.has_node(link)):
        networkTopology.add_node(host)
        log.info("host " + host.id + " adicionado ao grado de topologia")
        networkTopology.add_edge(link, host, object = edge, weight = 1)
        log.info("switch " + link.id + " conectado ao host " + host.id + " na porta " + edge.port1)

def launch ():
    multicastController.addMember("10.0.0.1", "1.1.1.1")
    multicastController.addMember("10.0.0.2", "1.1.1.1")
    multicastController.addMember("10.0.0.3", "1.1.1.1")
    
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)
    core.host_tracker.addListenerByName("HostEvent", _handle_HostEvent)
    log.info("controlador iniciado")



"""
Frederico Sales <frederico.sales@engenharia.ufjf.br>
Engenharia Computacional - 201765803B
Tópicos de Redes e Processamento Distribuido II
POX  - Mininet firewall reativo

# Mininet
$ sudo mn --topo single,3 --mac --controller remote -x

# Pox
$ sudo ./pox.py firewall_reativo forwarding.l2_pairs info.packet_dump samples.pretty_log log.level --DEBUG
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

def _handle_PacketIn(event):
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr("00:00:00:00:00:01")
    msg.match.dl_type = 0x800
    msg.match.nw_dst = IPAddr("10.0.0.3")
    event.connection.send(msg)

    log.info("firewall reativo ativado no Switch: %s", dpidToStr(event.dpid))

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("firewall_reativo ativado.")

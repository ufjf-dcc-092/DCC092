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
from pox.lib.addresses import IPaddr, EthAddr

log = core.getLogger()

def _handle_ConnectionUp(event):
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr("00:00:00:00:00:01")
    msg.match.dl_type = 0x800
    msg.match.nw_dst = IPaddr("10.0.0.3")
    event.connection.send(msg)

    log.info("Firewall proativo ativado no  Switch %s", dpidToStr(event.dipid))

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("firewall_proativo ativado")

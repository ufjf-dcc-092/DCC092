#O controlador de forma proativa instala regras na tabela de fluxo do(s) switches openflow quando e realizada uma conexao com um Switch. Utiliza-se para este objetivo o evento ConnectionUP

#importacao de bibliotecas
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

#Quando e realizada uma conexao com um Switch, um evento ConnectionUp e disparado.

def _handle_ConnectionUp(event):
	#metodo para criar uma mensagem de modificacao da tabela de fluxos
	msg = of.ofp_flow_mod()
	##CONFIGURACAO DAS REGRAS dl_src(mac de origem)
	msg.match.dl_src = EthAddr("00:00:00:00:00:01")

	#regra para filtrar pacotes ip
	msg.match.dl_type = 0x800
	#msg.match.nw_proto = 17
	#endereco ip especifico
	msg.match.nw_dst = IPAddr("10.0.0.3")
	#aqui deveriamos colocar uma acao como esta:msg.actions.append(of.ofp_action_output(port=2)) porem como queremos descartar os pacotes, criaremos uma regra sem acao
	#envio da mensagem openflow para o switch:
	event.connection.send(msg)

	log.info("firewall proativo ativado no Switch: %s", dpidToStr(event.dpid))

#funcao de lancanto
def launch():
	#Habilita o componente a ouvir ao evento ConnectionUp
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
	log.info("firewall_proativo ativado.")

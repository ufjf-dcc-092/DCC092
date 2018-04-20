# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
#msg1 = of.ofp_flow_mod()
#msg1.match.dl_type = 0x800
#msg1.match.dl_src = EthAddr("f6:2a:40:9c:ab:e2")
#msg1.match.dl_dst = EthAddr("86:97:e1:c7:60:d5")
#msg1.actions.append(of.ofp_action_output(port=1))
#event.connection.send(msg1)"
#Funcao que envia uma mensagem openflow para um Switch
#event.connection.send(msg)
#msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
#msg.priority = 42
#msg.match.dl_type = 0x800
#msg.match.nw_dst = IPAddr("10.0.0.2")
#msg.match.tp_dst = 80
#msg.actions.append(of.ofp_action_output(port=2))
#Criar uma regra sem saida, faz com que o fluxo seja dropado
#msg.actions.append(of.ofp_action_output(port = 99))
#msg = of.ofp_packet_out()
#dl_dst(mac address de destino)
#msg.match.dl_dst = EthAddr("00:00:00:00:00:03")

"""
Created on Apr 19 2018
Modificado por: Michel

O controlador, de forma reativa, instala regras na tabela de fluxo do(s) switches openflow quando e realizada uma conexao com um Switch. Utiliza-se para este objetivo o evento ConnectionUp.
"""
#importacao de bibbliotcas
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

#Quando e realizada uma conexao com um Switch, um evento ConnectionUP e disparado.
def _handle_ConnectionUp (event):
 
    #metodo para cirar uma mensagem de modificacao da tabela de fluxos do switch
    msg = of.ofp_flow_mod()
    #CONFIGURACAO DAS REGRAS dl_src(mac de origem)
    msg.match.dl_src = EthAddr("00:00:00:00:00:01")    
    
    #regra para filtrar pacotes do PROTOCOLO ip
    msg.match.dl_type = 0x800
    #msg.match.nw_proto = 17
    #endereco ip especifico
    msg.match.nw_dst = IPAddr("10.0.0.3")     
    
    event.connection.send(msg)
    
    log.info("firewall reativo ativado no Switch: %s", dpidToStr(event.dpid))

#funcao de lancamento
def launch ():
    #Habilita o componente a ouvir ao evento ConnectionUp  
    core.openflow.addListenerByName("PacketIn", _handle_ConnectionUp)
    log.info("firewall_reativo ativado.")



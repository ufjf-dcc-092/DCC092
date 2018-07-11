import sys

from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info, warn

def startNetwork():
    net = Mininet( controller=Controller )
    
    info( '*** Adding controller\n' )
    net.addController( 'c0' )
        
    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    h3 = net.addHost( 'h3', ip='10.0.0.3' )
    h4 = net.addHost( 'h4', ip='10.0.0.4' )
    h5 = net.addHost( 'h5', ip='10.0.0.5' )
    server = net.addHost( 'server', ip='10.0.0.11' )
    
    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )
    s5 = net.addSwitch( 's5' )
        
    info( '*** Creating links\n' )
    net.addLink( s1, s2 )
    net.addLink( s1, s4 )
    net.addLink( s2, s3 )
    net.addLink( s2, h2 )
    net.addLink( s2, s4 )
    net.addLink( s3, h1 )
    net.addLink( s3, h5 )
    net.addLink( s4, s5 )
    net.addLink( s4, h3 )
    net.addLink( s5, h4 )
    net.addLink( s1, server )
    
    info( '*** Starting network\n' )
    net.start()

if __name__ == '__main__':
    startNetwork()
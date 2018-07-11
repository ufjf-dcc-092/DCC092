from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI
"""
Instructions to run the topo:
    1. Go to directory where this fil is.
    2. run: sudo -E python Simple_Pkt_Topo.py.py

The topo has 4 switches and 4 hosts. They are connected in a star shape.
"""


class SimplePktSwitch(Topo):
    """Simple topology example."""

    def __init__(self, **opts):
        """Create custom topo."""

        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(SimplePktSwitch, self).__init__(**opts)

        # Add hosts and switches
        info( '*** Adding hosts\n' )
        h1 = self.addHost('h1', ip="10.0.0.1")
        h2 = self.addHost('h2', ip="10.0.0.2")
        h3 = self.addHost('h3', ip="10.0.0.3")
        h4 = self.addHost('h4', ip="10.0.0.4")
        h5 = self.addHost('h5', ip="10.0.0.5")
        server = self.addHost('server', ip="10.0.0.11")

        # Adding switches
        info( '*** Adding switch\n' )
        s1 = self.addSwitch('s1', dpid="0000000000000001")
        s2 = self.addSwitch('s2', dpid="0000000000000002")
        s3 = self.addSwitch('s3', dpid="0000000000000003")
        s4 = self.addSwitch('s4', dpid="0000000000000004")
        s5 = self.addSwitch('s5', dpid="0000000000000005")

        # Add links
        info( '*** Creating links\n' )
        self.addLink( s1, s2 )
        self.addLink( s1, s4 )
        self.addLink( s2, s3 )
        self.addLink( s2, h2 )
        self.addLink( s2, s4 )
        self.addLink( s3, h1 )
        self.addLink( s3, h5 )
        self.addLink( s4, s5 )
        self.addLink( s4, h3 )
        self.addLink( s5, h4 )
        self.addLink( s1, server )


def run():
    c0 = RemoteController('c0', '0.0.0.0', 6633)
    net = Mininet(topo=SimplePktSwitch(), host=CPULimitedHost, controller=None)
    net.addController(c0)
    info( '*** Starting network\n' )
    net.start()

    CLI(net)
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()
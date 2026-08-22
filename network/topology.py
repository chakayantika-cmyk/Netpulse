import networkx as nx


def create_network():
    """
    Create the initial NetPulse network topology.

    Each network link contains five important
    network-health metrics:

    - latency
    - utilization
    - packet_loss
    - jitter
    - queue_length
    """

    network = nx.Graph()

    # -------------------------------------------------
    # Add routers
    # -------------------------------------------------

    routers = ["R1", "R2", "R3", "R4", "R5"]

    for router in routers:
        network.add_node(router)

    # -------------------------------------------------
    # Add network links and metrics
    # -------------------------------------------------

    network.add_edge(
        "R1",
        "R2",
        latency=10,          # milliseconds
        utilization=45,     # percentage
        packet_loss=1.0,    # percentage
        jitter=2,           # milliseconds
        queue_length=20     # packets
    )

    network.add_edge(
        "R1",
        "R3",
        latency=20,
        utilization=35,
        packet_loss=0.5,
        jitter=3,
        queue_length=15
    )

    network.add_edge(
        "R2",
        "R4",
        latency=15,
        utilization=60,
        packet_loss=2.0,
        jitter=4,
        queue_length=30
    )

    network.add_edge(
        "R3",
        "R4",
        latency=10,
        utilization=40,
        packet_loss=1.0,
        jitter=2,
        queue_length=18
    )

    network.add_edge(
        "R4",
        "R5",
        latency=10,
        utilization=50,
        packet_loss=1.0,
        jitter=2,
        queue_length=25
    )

    return network


def display_network(network):
    """
    Display the NetPulse network topology
    and the health metrics of every link.
    """

    print("\n========================================")
    print("       NetPulse Network Topology")
    print("========================================\n")

    print("Routers:")
    for router in network.nodes:
        print(f"  - {router}")

    print("\nNetwork Links:\n")

    for source, destination, data in network.edges(data=True):

        print(f"{source} <--> {destination}")

        print(f"  Latency       : {data['latency']} ms")
        print(f"  Utilization   : {data['utilization']} %")
        print(f"  Packet Loss   : {data['packet_loss']} %")
        print(f"  Jitter        : {data['jitter']} ms")
        print(f"  Queue Length  : {data['queue_length']} packets")

        print("----------------------------------------")


def find_routes(network, source, destination):
    """
    Find all possible routes between two routers.
    """

    print(
        f"\nPossible routes from {source} to {destination}:\n"
    )

    routes = list(
        nx.all_simple_paths(
            network,
            source=source,
            target=destination
        )
    )

    for number, route in enumerate(routes, start=1):

        print(
            f"  Route {number}: "
            f"{' -> '.join(route)}"
        )

    return routes


if __name__ == "__main__":

    # Create the NetPulse network
    netpulse_network = create_network()

    # Display network topology and metrics
    display_network(netpulse_network)

    # Find possible routes
    find_routes(
        netpulse_network,
        "R1",
        "R5"
    )
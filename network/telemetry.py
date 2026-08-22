import random
import time

try:
    from .topology import create_network
except ImportError:
    from topology import create_network
class TelemetrySimulator:
    """
    Simulates changing network telemetry for NetPulse.

    Metrics:
    - Latency
    - Utilization
    - Packet Loss
    - Jitter
    - Queue Length
    """

    def __init__(self, network):
        self.network = network

    def update_link(self, source, destination):
        """Generate a new telemetry reading for one network link."""

        link = self.network[source][destination]

        # Current values
        current_latency = link["latency"]
        current_utilization = link["utilization"]
        current_jitter = link["jitter"]
        current_queue = link["queue_length"]

        # -----------------------------
        # 1. Utilization
        # -----------------------------

        utilization_change = random.uniform(-8, 8)

        new_utilization = (
            current_utilization + utilization_change
        )

        new_utilization = max(
            0,
            min(100, new_utilization)
        )

        # -----------------------------
        # 2. Latency
        # -----------------------------

        latency_change = random.uniform(-2, 2)

        new_latency = (
            current_latency + latency_change
        )

        new_latency = max(
            1,
            new_latency
        )

        # -----------------------------
        # 3. Jitter
        # -----------------------------

        jitter_change = random.uniform(-0.8, 0.8)

        new_jitter = (
            current_jitter + jitter_change
        )

        new_jitter = max(
            0,
            new_jitter
        )

        # -----------------------------
        # 4. Queue Length
        # -----------------------------

        queue_change = random.randint(-5, 5)

        new_queue = (
            current_queue + queue_change
        )

        new_queue = max(
            0,
            new_queue
        )

        # -----------------------------
        # 5. Packet Loss
        # -----------------------------

        # Higher utilization generally
        # produces higher packet loss.

        if new_utilization > 80:

            new_packet_loss = random.uniform(
                2,
                6
            )

        elif new_utilization > 60:

            new_packet_loss = random.uniform(
                1,
                3
            )

        else:

            new_packet_loss = random.uniform(
                0,
                1.5
            )

        # -----------------------------
        # Save new values
        # -----------------------------

        link["latency"] = round(
            new_latency,
            2
        )

        link["utilization"] = round(
            new_utilization,
            2
        )

        link["packet_loss"] = round(
            new_packet_loss,
            2
        )

        link["jitter"] = round(
            new_jitter,
            2
        )

        link["queue_length"] = new_queue

    def update_all_links(self):
        """Update telemetry for every network link."""

        for source, destination in self.network.edges():

            self.update_link(
                source,
                destination
            )

    def display_telemetry(self):
        """Display current telemetry values."""

        print("\n========================================")
        print("        NetPulse Live Telemetry")
        print("========================================\n")

        for source, destination, data in self.network.edges(
            data=True
        ):

            print(
                f"{source} <--> {destination}"
            )

            print(
                f"  Latency      : "
                f"{data['latency']} ms"
            )

            print(
                f"  Utilization  : "
                f"{data['utilization']} %"
            )

            print(
                f"  Packet Loss  : "
                f"{data['packet_loss']} %"
            )

            print(
                f"  Jitter       : "
                f"{data['jitter']} ms"
            )

            print(
                f"  Queue Length : "
                f"{data['queue_length']} packets"
            )

            print("----------------------------------------")


def run_simulation():

    # Create the network topology
    network = create_network()

    # Create telemetry simulator
    simulator = TelemetrySimulator(network)

    # Run for 10 time steps
    for step in range(1, 11):

        print(
            f"\n\n========== TIME STEP {step} =========="
        )

        # Update all network links
        simulator.update_all_links()

        # Display current telemetry
        simulator.display_telemetry()

        # Wait one second
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()
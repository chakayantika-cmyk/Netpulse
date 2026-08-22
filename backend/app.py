import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from flask import Flask, jsonify
from flask_cors import CORS

from network.topology import create_network
from network.telemetry import TelemetrySimulator


app = Flask(__name__)
CORS(app)


# --------------------------------------------------
# Create the NetPulse network
# --------------------------------------------------

network = create_network()

# Create the telemetry simulator
simulator = TelemetrySimulator(network)


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "project": "NetPulse",
        "status": "online",
        "message": "NetPulse backend is running"
    })


# --------------------------------------------------
# Topology endpoint
# --------------------------------------------------

@app.route("/api/topology")
def get_topology():

    routers = list(network.nodes)

    links = []

    for source, destination, data in network.edges(
        data=True
    ):

        links.append({
            "source": source,
            "destination": destination,
            "latency": data["latency"],
            "utilization": data["utilization"],
            "packet_loss": data["packet_loss"],
            "jitter": data["jitter"],
            "queue_length": data["queue_length"]
        })

    return jsonify({
        "routers": routers,
        "links": links
    })


# --------------------------------------------------
# Live telemetry endpoint
# --------------------------------------------------

@app.route("/api/telemetry")
def get_telemetry():

    # Generate a new telemetry reading
    simulator.update_all_links()

    links = []

    for source, destination, data in network.edges(
        data=True
    ):

        links.append({
            "source": source,
            "destination": destination,
            "latency": data["latency"],
            "utilization": data["utilization"],
            "packet_loss": data["packet_loss"],
            "jitter": data["jitter"],
            "queue_length": data["queue_length"]
        })

    return jsonify({
        "links": links
    })


# --------------------------------------------------
# Run Flask
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
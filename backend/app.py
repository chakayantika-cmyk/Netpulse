import sys
import os
from datetime import datetime

# --------------------------------------------------
# Allow Python to find the network package
# --------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from flask import Flask, jsonify, request
from flask_cors import CORS

from network.topology import create_network
from network.telemetry import TelemetrySimulator


# ==================================================
# CREATE FLASK APPLICATION
# ==================================================

app = Flask(__name__)

CORS(app)


# ==================================================
# CREATE NETPULSE NETWORK
# ==================================================

network = create_network()

simulator = TelemetrySimulator(network)


# ==================================================
# HELPER: GET LINKS
# ==================================================

def get_links():

    links = []

    for source, destination, data in network.edges(data=True):

        links.append({

            "source": source,

            "destination": destination,

            "latency": round(data["latency"], 2),

            "utilization": round(data["utilization"], 2),

            "packet_loss": round(data["packet_loss"], 2),

            "jitter": round(data["jitter"], 2),

            "queue_length": round(data["queue_length"], 2)

        })

    return links


# ==================================================
# HELPER: CALCULATE AVERAGES
# ==================================================

def calculate_averages(links):

    if not links:

        return {
            "latency": 0,
            "utilization": 0,
            "packet_loss": 0,
            "jitter": 0,
            "queue_length": 0
        }

    return {

        "latency": sum(
            link["latency"]
            for link in links
        ) / len(links),

        "utilization": sum(
            link["utilization"]
            for link in links
        ) / len(links),

        "packet_loss": sum(
            link["packet_loss"]
            for link in links
        ) / len(links),

        "jitter": sum(
            link["jitter"]
            for link in links
        ) / len(links),

        "queue_length": sum(
            link["queue_length"]
            for link in links
        ) / len(links)

    }


# ==================================================
# NETWORK HEALTH
# ==================================================

def calculate_network_health(links):

    if not links:

        return 0

    averages = calculate_averages(links)

    health = (

        100

        - (averages["latency"] * 0.2)

        - (averages["utilization"] * 0.3)

        - (averages["packet_loss"] * 5)

        - (averages["jitter"] * 0.5)

        - (averages["queue_length"] * 0.2)

    )

    health = max(
        0,
        min(
            100,
            health
        )
    )

    return round(
        health,
        2
    )


# ==================================================
# ANOMALY SCORE
# ==================================================

def calculate_anomaly_score(averages):

    latency_score = min(
        averages["latency"] / 100,
        1
    )

    utilization_score = min(
        averages["utilization"] / 100,
        1
    )

    packet_loss_score = min(
        averages["packet_loss"] / 10,
        1
    )

    jitter_score = min(
        averages["jitter"] / 20,
        1
    )

    queue_score = min(
        averages["queue_length"] / 50,
        1
    )

    score = (

        latency_score * 0.25

        + utilization_score * 0.25

        + packet_loss_score * 0.20

        + jitter_score * 0.15

        + queue_score * 0.15

    )

    return round(
        max(
            0,
            min(
                1,
                score
            )
        ),
        2
    )


# ==================================================
# RISK LEVEL
# ==================================================

def get_risk_level(score):

    if score < 0.35:

        return "LOW"

    elif score < 0.65:

        return "MODERATE"

    else:

        return "HIGH"


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return jsonify({

        "project": "NetPulse",

        "status": "online",

        "message":
            "NetPulse Flask API is running",

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/api/health")
def health_check():

    return jsonify({

        "success": True,

        "service": "NetPulse Flask API",

        "status": "healthy",

        "routers":
            len(network.nodes),

        "links":
            len(network.edges),

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# TOPOLOGY
# ==================================================

@app.route("/api/topology")
def get_topology():

    return jsonify({

        "success": True,

        "routers":
            list(network.nodes),

        "links":
            get_links()

    })


# ==================================================
# LIVE TELEMETRY
# ==================================================

@app.route("/api/telemetry")
def get_telemetry():

    simulator.update_all_links()

    links = get_links()

    return jsonify({

        "success": True,

        "timestamp":
            datetime.now().isoformat(),

        "links": links

    })


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/api/dashboard")
def get_dashboard():

    simulator.update_all_links()

    links = get_links()

    averages = calculate_averages(
        links
    )

    health = calculate_network_health(
        links
    )

    anomaly_score = calculate_anomaly_score(
        averages
    )

    risk_level = get_risk_level(
        anomaly_score
    )

    return jsonify({

        "success": True,

        "project": "NetPulse",

        "status": (

            "healthy"

            if health >= 70

            else "warning"

        ),

        "network_health": health,

        "anomaly_score":
            anomaly_score,

        "risk_level":
            risk_level,

        "mean_time_to_predict": 4.2,

        "routers":
            len(network.nodes),

        "links":
            len(network.edges),

        "averages": {

            "latency":
                round(
                    averages["latency"],
                    2
                ),

            "utilization":
                round(
                    averages["utilization"],
                    2
                ),

            "packet_loss":
                round(
                    averages["packet_loss"],
                    2
                ),

            "jitter":
                round(
                    averages["jitter"],
                    2
                ),

            "queue_length":
                round(
                    averages["queue_length"],
                    2
                )

        },

        "telemetry":
            links,

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# PREDICTION
# ==================================================

@app.route("/api/prediction")
def prediction():

    simulator.update_all_links()

    links = get_links()

    averages = calculate_averages(
        links
    )

    anomaly_score = calculate_anomaly_score(
        averages
    )

    risk_level = get_risk_level(
        anomaly_score
    )

    # ----------------------------------------------
    # Prediction
    # ----------------------------------------------

    if anomaly_score >= 0.70:

        prediction_result = "critical"

        confidence = round(
            anomaly_score * 100
        )

    elif anomaly_score >= 0.45:

        prediction_result = "degrading"

        confidence = round(
            anomaly_score * 100
        )

    else:

        prediction_result = "stable"

        confidence = round(
            (1 - anomaly_score) * 100
        )

    return jsonify({

        "success": True,

        "prediction":
            prediction_result,

        "confidence":
            confidence,

        "risk_level":
            risk_level,

        "anomaly_score":
            anomaly_score,

        "current_latency_ms":
            round(
                averages["latency"],
                2
            ),

        "current_utilization_percent":
            round(
                averages["utilization"],
                2
            ),

        "packet_loss_percent":
            round(
                averages["packet_loss"],
                2
            ),

        "jitter_ms":
            round(
                averages["jitter"],
                2
            ),

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# ANOMALIES
# ==================================================

@app.route("/api/anomalies")
def anomalies():

    simulator.update_all_links()

    links = get_links()

    detected = []

    for link in links:

        problems = []

        if link["latency"] > 100:

            problems.append(
                "High latency"
            )

        if link["utilization"] > 80:

            problems.append(
                "High utilization"
            )

        if link["packet_loss"] > 5:

            problems.append(
                "High packet loss"
            )

        if link["jitter"] > 20:

            problems.append(
                "High jitter"
            )

        if link["queue_length"] > 50:

            problems.append(
                "Queue congestion"
            )

        if problems:

            detected.append({

                "source":
                    link["source"],

                "destination":
                    link["destination"],

                "problems":
                    problems,

                "severity":
                    "HIGH"

            })

    return jsonify({

        "success": True,

        "count":
            len(detected),

        "anomalies":
            detected,

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# RUN FLASK
# ==================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
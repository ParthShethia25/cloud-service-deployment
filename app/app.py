from flask import Flask, jsonify, request
import random
import logging
import time

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy"), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify(status="ready"), 200

@app.route("/apply-loan", methods=["POST"])
def apply_loan():
    payload = request.json or {}
    applicant = payload.get("applicant", "unknown")

    logging.info(f"Loan request received for applicant={applicant}")

    time.sleep(1)

    if random.random() < 0.2:
        logging.error("Simulated processing failure")
        return jsonify(error="processing failed"), 500

    logging.info("Loan processed successfully")
    return jsonify(result="approved"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

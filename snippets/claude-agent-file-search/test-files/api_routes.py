"""API route definitions for the web service."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "api-server"})


@app.route("/api/users", methods=["GET"])
def list_users():
    """List all users."""
    # TODO: Implement user listing from database
    return jsonify({"users": []})


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID."""
    # TODO: Fetch user from database
    return jsonify({"user_id": user_id, "username": "example"})


@app.route("/api/products", methods=["GET"])
def list_products():
    """List all products with pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    # TODO: Implement product listing with pagination
    return jsonify({
        "products": [],
        "page": page,
        "per_page": per_page,
        "total": 0
    })


@app.route("/api/orders", methods=["POST"])
def create_order():
    """Create a new order."""
    _data = request.get_json()
    # TODO: Validate and save order data
    return jsonify({"order_id": "12345", "status": "pending"}), 201


if __name__ == "__main__":
    app.run(debug=True, port=8000)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Note N Go backend is running"

@app.route("/upload", methods=["POST"])
def upload():
    return jsonify({"message": "Upload received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

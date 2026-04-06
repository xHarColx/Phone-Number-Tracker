import hashlib
from flask import Flask, Response

app = Flask(__name__)
track_id = "b21248a95057"

@app.route(f"/t/{track_id}")
def serve_tracking_page():
    return Response("Works!", mimetype="text/html")

print("Registered routes:")
print(app.url_map)

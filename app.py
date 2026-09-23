import sqlite3
import string
import os
from dotenv import load_dotenv
from hashids import Hashids
from flask import Flask, request, jsonify, redirect, abort, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import urlparse

load_dotenv()

HASHIDS_SALT = os.environ.get("HASHIDS_SALT")
hashids = Hashids(salt=HASHIDS_SALT, min_length = 6)
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)



def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

@app.route("/")
def home():
    return render_template("index.html")

#for HTML Form
@app.route("/shorten-form", methods = ["POST"])
@limiter.limit("10 per minute")
def shorten_form():
    original_url = request.form["url"]

    if not is_valid_url(original_url):
        return render_template("index.html", error="Invalid URL format")

    connection = sqlite3.connect("database.db")
    cursor = connection.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, "")
    )
    new_id = cursor.lastrowid
    
    short_code = hashids.encode(new_id)
    connection.execute(
        "UPDATE urls SET short_code = ? WHERE id = ?", (short_code, new_id)
    )

    connection.commit()
    connection.close()

    short_url = request.host_url + short_code
    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_to_url(short_code):
    connection = sqlite3.connect("database.db")
    cursor = connection.execute(
        "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
    )

    result = cursor.fetchone()
    connection.close()

    if result is None:
        abort(404)

    original_url = result[0]
    return redirect(original_url)

#for JSON API
@app.route("/shorten", methods=["POST"])
@limiter.limit("10 per minute")
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data["url"]

    if not is_valid_url(original_url):
            return jsonify("error", "Invalid URL format")
        
    connection = sqlite3.connect("database.db")
    cursor = connection.execute(
         "INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, "")
    )
    new_id = cursor.lastrowid

    short_code = hashids.encode(new_id)
    connection.execute(
         "UPDATE urls SET short_code = ? WHERE id = ?", (short_code, new_id)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("index.html", error="Too many requests. Please try again shortly."), 429



if __name__ == "__main__":
    app.run(debug = True)
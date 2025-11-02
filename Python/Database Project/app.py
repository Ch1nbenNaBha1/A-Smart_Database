# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import json
from secure_database import SecureDatabase  # your existing secure_database.py

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key in production

# Initialize your secure database
db = SecureDatabase()

# Dummy users for authentication
USERS = {"admin": "password"}  # Replace with hashed passwords in real apps

# ===== Authentication Decorator =====
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please login first!", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ===== Routes =====

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username] == password:
            session["user"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    records = list(db.get_all())
    return render_template("index.html", records=records, user=session["user"])

# ===== Add Record =====
@app.route("/add", methods=["POST"])
@login_required
def add_record():
    rid = request.form.get("record_id")
    rdata = request.form.get("record_data")
    try:
        # Attempt to parse JSON input if possible   
        rdata_json = json.loads(rdata)
    except:
        rdata_json = rdata  # Keep as string if not JSON
    db.add_record(rid, rdata_json)
    flash(f"Record '{rid}' added successfully!", "success")
    return redirect(url_for("index"))

# ===== Delete Record =====
@app.route("/delete/<record_id>")
@login_required
def delete_record(record_id):
    if db.delete_record(record_id):
        flash(f"Record '{record_id}' deleted!", "info")
    else:
        flash(f"Record '{record_id}' not found!", "error")
    return redirect(url_for("index"))

# ===== View Single Record =====
@app.route("/record/<record_id>")
@login_required
def view_record(record_id):
    record = db.get_record(record_id)
    if not record:
        flash(f"Record '{record_id}' not found!", "error")
        return redirect(url_for("index"))
    return render_template("record.html", record_id=record_id, record_data=record, user=session["user"])

# ===== Search Records =====
@app.route("/search")
@login_required
def search():
    query = request.args.get("q", "").lower()
    all_records = db.get_all()
    if query:
        filtered = [(rid, rdata) for rid, rdata in all_records
                    if query in rid.lower() or query in str(rdata).lower()]
    else:
        filtered = list(all_records)
    return render_template("index.html", records=filtered, user=session["user"])

# ===== Upload JSON =====
@app.route("/upload", methods=["POST"])
@login_required
def upload_json():
    file = request.files.get("json_file")
    if not file:
        flash("No file uploaded!", "error")
        return redirect(url_for("index"))
    
    try:
        data = json.load(file)
        added = 0
        skipped = 0

        # Handle dictionary JSON
        if isinstance(data, dict):
            for rid, rdata in data.items():
                if rid in db.get_all():
                    skipped += 1
                    continue
                db.add_record(rid, rdata)
                added += 1

        # Handle list of records: [{"id": "...", "data": ...}]
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "id" in item and "data" in item:
                    rid = item["id"]
                    rdata = item["data"]
                    if rid in db.get_all():
                        skipped += 1
                        continue
                    db.add_record(rid, rdata)
                    added += 1
                else:
                    skipped += 1
        flash(f"JSON processed! Added: {added}, Skipped (duplicates/invalid): {skipped}", "success")
    except Exception as e:
        flash(f"Error processing JSON: {str(e)}", "error")
    
    return redirect(url_for("index"))

# ===== Run App =====
if __name__ == "__main__":
    app.run(debug=True)

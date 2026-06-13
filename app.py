import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------------------------
# Database Configuration
# ---------------------------

database_url = os.environ.get("DATABASE_URL")

if database_url:
    # Render PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )
else:
    # Local PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@localhost/infx_db"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

# ---------------------------
# User Model
# ---------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

# ---------------------------
# Create Tables
# ---------------------------

with app.app_context():
    db.create_all()

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")

        if not fullname or not email or not password:
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already exists"
            }), 400

        user = User(
            fullname=fullname,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful"
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ---------------------------
# Run App
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
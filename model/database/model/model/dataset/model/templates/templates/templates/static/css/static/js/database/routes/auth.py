from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth = Blueprint("auth", __name__)

DATABASE = "database/database.db"


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """, (username, email, hashed_password))

            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            return render_template(
                "register.html",
                error="User already exists"
            )

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE username=?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[3],
            password
        ):

            session["username"] = username

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid Credentials"
        )

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")

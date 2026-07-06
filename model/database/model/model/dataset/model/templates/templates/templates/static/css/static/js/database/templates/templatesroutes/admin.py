from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3
from functools import wraps

admin = Blueprint("admin", __name__)

DATABASE = "database/database.db"

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Admin Login Required
# -----------------------------
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect("/admin/login")
        return func(*args, **kwargs)
    return wrapper


# -----------------------------
# Admin Login
# -----------------------------
@admin.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Change these credentials before deployment
        if username == "admin" and password == "admin123":

            session["admin"] = username

            return redirect("/admin/dashboard")

        flash("Invalid Admin Credentials", "danger")

    return render_template("admin_login.html")


# -----------------------------
# Admin Logout
# -----------------------------
@admin.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin/login")


# -----------------------------
# Dashboard
# -----------------------------
@admin.route("/admin/dashboard")
@admin_required
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM history")
    total_predictions = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE prediction='Fake News'
    """)
    fake_count = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE prediction='Real News'
    """)
    real_count = cur.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions,
        fake_count=fake_count,
        real_count=real_count
    )


# -----------------------------
# View Users
# -----------------------------
@admin.route("/admin/users")
@admin_required
def users():

    conn = get_connection()

    users = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "manage_users.html",
        users=users
    )


# -----------------------------
# Delete User
# -----------------------------
@admin.route("/admin/delete_user/<int:user_id>")
@admin_required
def delete_user(user_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    flash("User Deleted Successfully", "success")

    return redirect("/admin/users")


# -----------------------------
# Prediction History
# -----------------------------
@admin.route("/admin/history")
@admin_required
def history():

    conn = get_connection()

    history = conn.execute("""
        SELECT *
        FROM history
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "manage_predictions.html",
        history=history
    )


# -----------------------------
# Delete Prediction
# -----------------------------
@admin.route("/admin/delete_prediction/<int:id>")
@admin_required
def delete_prediction(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM history WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash(
        "Prediction Deleted Successfully",
        "success"
    )

    return redirect("/admin/history")


# -----------------------------
# Search User
# -----------------------------
@admin.route("/admin/search", methods=["POST"])
@admin_required
def search():

    keyword = request.form["keyword"]

    conn = get_connection()

    users = conn.execute("""
        SELECT *
        FROM users
        WHERE username LIKE ?
        OR email LIKE ?
    """,
    (
        "%" + keyword + "%",
        "%" + keyword + "%"
    )
    ).fetchall()

    conn.close()

    return render_template(
        "manage_users.html",
        users=users
    )

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "expenses.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            category TEXT,
            type TEXT
        )
    """)

    # Check if table empty
    data = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]

    if data == 0:
        conn.execute("""
        INSERT INTO expenses (title, amount, category, type) VALUES
        ('Food', 200, 'Groceries', 'Expense'),
        ('Travel', 500, 'Bus', 'Expense'),
        ('Salary', 15000, 'Job', 'Income')
        """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    expenses = conn.execute("SELECT * FROM expenses ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add_expense():
    data = request.get_json()

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, type) VALUES (?,?,?,?)",
        (data["title"], data["amount"], data["category"], data["type"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Added"})


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


@app.route("/summary")
def summary():
    conn = get_db()

    expense = conn.execute(
        "SELECT SUM(amount) FROM expenses WHERE type='Expense'"
    ).fetchone()[0] or 0

    income = conn.execute(
        "SELECT SUM(amount) FROM expenses WHERE type='Income'"
    ).fetchone()[0] or 0

    conn.close()

    return jsonify({
        "expense": expense,
        "income": income
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                issue TEXT,
                status TEXT DEFAULT 'Open'
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_ticket():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (name, email, issue) VALUES (?, ?, ?)", (name, email, issue))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
    return render_template('admin.html', tickets=tickets)

@app.route('/close_ticket/<int:ticket_id>')
def close_ticket(ticket_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status='Closed' WHERE id=?", (ticket_id,))
        conn.commit()
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)
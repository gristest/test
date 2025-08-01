
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(os.path.dirname(__file__), '../database/chat.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                content TEXT NOT NULL,
                is_user BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (id)
            )
        ''')
        db.commit()

@app.route('/api/chats', methods=['GET'])
def get_chats():
    db = get_db()
    chats = db.execute('SELECT * FROM chats ORDER BY created_at DESC').fetchall()
    return jsonify([dict(chat) for chat in chats])

@app.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO chats (title) VALUES (?)', [data.get('title', 'New Chat')])
    db.commit()
    return jsonify({'id': cursor.lastrowid, 'title': data.get('title', 'New Chat')}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

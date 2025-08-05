
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../db/chat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/conversations', methods=['GET'])
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'created_at': c.created_at} for c in conversations])

@app.route('/conversations', methods=['POST'])
def create_conversation():
    new_conv = Conversation(name="New Conversation")
    db.session.add(new_conv)
    db.session.commit()
    return jsonify({'id': new_conv.id, 'name': new_conv.name}), 201

@app.route('/conversations/<int:conv_id>', methods=['GET'])
def get_conversation(conv_id):
    conversation = Conversation.query.get_or_404(conv_id)
    messages = [{'id': m.id, 'content': m.content, 'is_user': m.is_user} for m in conversation.messages]
    return jsonify({'id': conversation.id, 'name': conversation.name, 'messages': messages})

@app.route('/conversations/<int:conv_id>/messages', methods=['POST'])
def add_message(conv_id):
    conversation = Conversation.query.get_or_404(conv_id)
    data = request.get_json()
    new_message = Message(content=data['content'], is_user=data.get('is_user', True), conversation_id=conv_id)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'id': new_message.id, 'content': new_message.content}), 201

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(basedir, '../uploads', filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

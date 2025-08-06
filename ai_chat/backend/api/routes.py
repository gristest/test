

from flask import Blueprint, jsonify, request
from models import db, Conversation, Message
from datetime import datetime

conversation_routes = Blueprint('conversations', __name__, url_prefix='/api/conversations')

@conversation_routes.route('/', methods=['GET'])
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([{'id': conv.id, 'title': conv.title} for conv in conversations])

@conversation_routes.route('/', methods=['POST'])
def create_conversation():
    new_conv = Conversation(title=f"New Chat {datetime.now().strftime('%m/%d %H:%M')}")
    db.session.add(new_conv)
    db.session.commit()
    return jsonify({'id': new_conv.id, 'title': new_conv.title})

@conversation_routes.route('/<int:conv_id>', methods=['GET'])
def get_conversation(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    return jsonify({
        'id': conv.id,
        'title': conv.title,
        'messages': [{
            'content': msg.content,
            'sender': msg.sender,
            'timestamp': msg.timestamp.isoformat()
        } for msg in conv.messages]
    })

@conversation_routes.route('/<int:conv_id>/messages', methods=['POST'])
def add_message(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    data = request.json
    
    # Add user message
    user_msg = Message(
        content=data.get('content'),
        sender='user',
        conversation_id=conv_id
    )
    db.session.add(user_msg)
    
    # Add AI response
    ai_msg = Message(
        content=f"Response to: {data.get('content')}",
        sender='ai', 
        conversation_id=conv_id
    )
    db.session.add(ai_msg)
    
    db.session.commit()
    return jsonify({'status': 'success'})


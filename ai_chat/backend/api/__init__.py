
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock conversation data
conversations = {}
current_id = 1

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    return jsonify([{'id': k, 'title': v['title']} for k,v in conversations.items()])

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    global current_id
    conv_id = str(current_id)
    conversations[conv_id] = {
        'title': f'New Chat {current_id}',
        'messages': []
    }
    current_id += 1
    return jsonify({'id': conv_id, 'title': conversations[conv_id]['title']})

@app.route('/api/conversations/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    return jsonify(conversations.get(conv_id, {}))

@app.route('/api/conversations/<conv_id>/messages', methods=['POST'])
def add_message(conv_id):
    data = request.json
    if conv_id in conversations:
        conversations[conv_id]['messages'].append({
            'content': data.get('content'),
            'sender': 'user'
        })
        # Add mock AI response
        conversations[conv_id]['messages'].append({
            'content': f"This is a mock response to: {data.get('content')}",
            'sender': 'ai'
        })
    return jsonify({'status': 'success'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Mock file upload response
    return jsonify({
        'status': 'success',
        'filename': 'mock_upload.txt'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

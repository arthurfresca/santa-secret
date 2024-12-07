from flask import Flask, request, jsonify
import base64
import random
import json

def encrypt(text):
    # Encripta o texto usando base64
    encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return encoded

def decrypt(encoded_text):
    # Decripta o texto codificado em base64
    decoded = base64.b64decode(encoded_text).decode('utf-8')
    return decoded

app = Flask(__name__)

@app.route('/generate-secret-santa', methods=['POST'])
def generate_secret_santa():
    data = request.json
    if not data or 'names' not in data:
        return jsonify({'error': 'Missing names in request body'}), 400

    names = data['names']
    if len(names) < 2:
        return jsonify({'error': 'At least two participants are required'}), 400

    # Shuffle para o sorteio
    shuffled = names[:]
    random.shuffle(shuffled)

    # Tornar o sorteio cíclico
    pairs = [(shuffled[i], shuffled[(i + 1) % len(shuffled)]) for i in range(len(shuffled))]

    # Gerar URLs com os nomes encriptados
    base_url = "https://arthurfresca.github.io/santa-secret/#"
    urls = []
    for giver, receiver in pairs:
        encrypted_receiver = encrypt(receiver)
        urls.append(f"{base_url}{giver}/{encrypted_receiver}")

    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64
from Crypto.Cipher import AES
import random
import base64
import json

def encrypt(text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    text_padded = text + (16 - len(text) % 16) * chr(16 - len(text) % 16)
    encrypted = cipher.encrypt(text_padded.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt(encrypted, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted)
    decrypted_padded = cipher.decrypt(encrypted_bytes).decode('utf-8')
    return decrypted_padded[:-ord(decrypted_padded[-1])]

key = "mysecretkey12345"  # Use uma chave de 16 caracteres

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
        encrypted_receiver = encrypt(receiver, key)
        urls.append(f"{base_url}{giver}/{encrypted_receiver}")

    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)
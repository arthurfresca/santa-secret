from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import random

app = Flask(__name__)

cipher = Fernet("wgk06QLqaTDl89NkOCqE44iibdJF19R-TkTsNFFZxSY=")

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
        encrypted_receiver = cipher.encrypt(receiver.encode()).decode()
        urls.append(f"{base_url}{giver}/{encrypted_receiver}")

    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)
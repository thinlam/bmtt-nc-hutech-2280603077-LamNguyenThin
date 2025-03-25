from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/caesar")
def caesar():
    return render_template("caesar.html")

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlaintext']
    key = int(request.form['inputKey'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"Text: {text}<br>Key: {key}<br>Encrypted Text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCiphertext']
    key = int(request.form['inputKey'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"Text: {text}<br>Key: {key}<br>Decrypted Text: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)

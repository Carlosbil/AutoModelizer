from flask import Flask, request, jsonify
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# path to save the files uploaded by the users
app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB as file limit

# if the folder doesnt exists, create one
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # see if the file has been sent
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    user = request.form.get('username')
    email = request.form.get('email')

    # if there is no user,  or email, send an error
    if not user or not email:
        return jsonify({"error": "User and email are required"}), 400

    # Si el usuario no selecciona un archivo, el navegador envía un archivo sin nombre
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.zip'):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "user": user,
            "email": email
        }), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)

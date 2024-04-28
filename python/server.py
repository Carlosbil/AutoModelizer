from flask import Flask, request, jsonify
import os
import zipfile
from flask_cors import CORS
from genetic import Genetic

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
    num_clases = request.form.get('num_clases')
    # if there is no user,  or email, send an error
    if not user or not email:
        return jsonify({"error": "User and email are required"}), 400

    # Si el usuario no selecciona un archivo, el navegador envía un archivo sin nombre
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.zip'):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Guardamos temporalmente el zip
        file.save(filepath)

        # creamos la ruta de extracción
        extract_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0])
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        # Descomprimimos el zip
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # y eliminamos el zip
        os.remove(filepath)
        
    else:
        return jsonify({"error": "Unsupported file type"}), 400
    
    # ahora que tenemos el csv guardado, toca crear los datasets
    algorithm = Genetic(num_classes=num_clases)
    train_loader, val_loader = algorithm.load_data(extract_path)
    population = algorithm.initialize_population()
    population_sol = algorithm.genetic_algorithm(population, train_loader, val_loader, device, max_desc, epochs)
    print()
    print()
    print("la sol es...")
    print(population_sol)
    
    return jsonify({
            "solution": population,
            "message": "File uploaded successfully",
            "filename": filename,
            "user": user,
            "email": email
        }), 200


if __name__ == '__main__':
    app.run(debug=True)

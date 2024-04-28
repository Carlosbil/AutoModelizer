from flask import Flask, request, jsonify
import os
import zipfile
from flask_cors import CORS, cross_origin
from genetic import Genetic
import torch
app = Flask(__name__)
CORS(app)

# path to save the files uploaded by the users
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024  # 16 MB as file limit

print("HELLO")
# if the folder doesnt exists, create one
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
            "message": "File uploaded successfully",
        }), 200
@app.route('/upload', methods=['POST'])
@cross_origin(origin='localhost:3000', headers=['Content-Type', 'Authorization'])
def upload_file():
    # see if the file has been sent
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    user = request.form.get('username')
    email = request.form.get('email')
    num_clases = int(request.form.get('num_clases'))
    maxDesc = int(request.form.get('numDesc'))
    epochs = int(request.form.get('numEpochs'))
    splitted = request.form.get('splitted')
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
    algorithm.check_cuda()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader = algorithm.load_data_image(extract_path) if splitted == "yes" else algorithm.load_data_image_not_splitted(extract_path)
    population = algorithm.initialize_population()
    population_sol = algorithm.genetic_algorithm(population, train_loader, val_loader, device, maxDesc, epochs)
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

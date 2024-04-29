from flask import Flask, request, jsonify
import os
import zipfile
from flask_cors import CORS, cross_origin
from genetic import Genetic
import torch
import threading
import json
app = Flask(__name__)
CORS(app)

# path to save the files uploaded by the users
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024  # 16 MB as file limit

file_path = 'datos.json'


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
    delete_json_file(file_path, email)
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
        thread = threading.Thread(target=algoritmo_gentico, args=(num_clases, extract_path, splitted, maxDesc, epochs, email))
        thread.start()
        return jsonify({"message": "Tarea iniciada"}), 202
    else:
        return jsonify({"error": "Unsupported file type"}), 400

def algoritmo_gentico(num_clases, extract_path, splitted, maxDesc, epochs, email):
        # ahora que tenemos el csv guardado, toca crear los datasets
    try:
        algorithm = Genetic(num_classes=num_clases)
        algorithm.check_cuda()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        train_loader, val_loader = algorithm.load_data_image(extract_path) if splitted == "yes" else algorithm.load_data_image_not_splitted(extract_path)
        population = algorithm.initialize_population()
        population_sol = algorithm.genetic_algorithm(population, train_loader, val_loader, device, maxDesc, epochs)
        update_json_file(file_path, {email: population[0]})
        print()
        print()
        print("la sol es...")
        print(population_sol)
    except:
        update_json_file(file_path, {email: {"error": "We couldn't complete your request"}})


    
def update_json_file(file_path, new_data):
    """
    Comprueba si existe un archivo JSON y lo actualiza.
    Si el archivo no existe, lo crea.
    
    :param file_path: Ruta al archivo JSON.
    :param new_data: Diccionario con los datos que se quieren añadir
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(new_data, file, indent=4)
        print("Archivo creado y datos añadidos.")
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        data.update(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("Datos actualizados.")

def delete_json_file(file_path, email):
    """
    Comprueba si existe un archivo JSON.
    Si el archivo no existe hecho
    Si el archivo existe y el email está, se borra
    
    :param file_path: Ruta al archivo JSON.
    :param email: info a eliminar
    """
    if not os.path.exists(file_path):
        return
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if email in data:
            del data[email]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("Datos eliminados si existían.")



def find_parameter_in_json(file_path, parameter_key):
    """
    Busca un parámetro específico en un archivo JSON.
    
    :param file_path: Ruta al archivo JSON.
    :param parameter_key: Clave del parámetro que se desea encontrar.
    :return: Valor del parámetro si se encuentra, None si no se encuentra o si hay un error.
    """
    try:
        if not os.path.exists(file_path):
            print("El archivo no existe.")
            return None
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if parameter_key in data:
            return data[parameter_key]
        else:
            print(f"Parámetro '{parameter_key}' no encontrado.")
            return None
        
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return None

@app.route('/result', methods=['POST'])
@cross_origin(origin='localhost:3000', headers=['Content-Type', 'Authorization'])
def get_result():

    user = request.form.get('username')
    email = request.form.get('email')
    # if there is no user,  or email, send an error
    if not user or not email:
        return jsonify({"error": "User and email are required"}), 400

    result = find_parameter_in_json(file_path, email)
    if result:
        return jsonify({"message": result}), 202
    else:
        return jsonify({"message":   {"Aux":"Still working on your submission"}}),200

    
if __name__ == '__main__':
    app.run(debug=True)

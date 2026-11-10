from flask import Flask, render_template, request, jsonify
from Arbol import procesar_respuestas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('PlantaHTML.html')

@app.route('/procesar_respuestas', methods=['POST'])
def procesar():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({'error': 'Se requiere un objeto JSON con las respuestas.'}), 400
    try:
        for campo in ['amin', 'altura', 'temp', 'ph']:
            if campo in datos:
                datos[campo] = float(datos[campo])
        for campo in ['estado', 'forma', 'herbacea', 'fruta', 'hoja', 'uso', 'cflor', 'heladas', 'riego', 'sol', 'velocidad', 'phCond', 'suelo', 'CMO']:
            if campo in datos:
                datos[campo] = int(datos[campo])

        resultado = procesar_respuestas(datos)
        return jsonify(resultado)
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from Arbol import procesar_respuestas

app = Flask(__name__)
    
@app.route('/')
def index():
    return render_template('PlantaHTML.html')

@app.route('/procesar_respuestas', methods=['POST'])
def procesar():
    datos = request.get_json()
    print("DATOS RECIBIDOS:", datos)
    try:
        # Forzar tipos numéricos seguros
        for campo in ["amin", "altura", "temp", "ph"]:
            if campo in datos:
                try:
                    datos[campo] = float(datos[campo])
                except:
                    pass
        for campo in ["estado", "forma", "herbacea", "fruta", "hoja", "uso", "cflor", "heladas", "riego", "sol", "velocidad", "phCond", "suelo", "CMO"]:
            if campo in datos:
                try:
                    datos[campo] = int(datos[campo])
                except:
                    pass

        imagen_url = procesar_respuestas(datos)

        return jsonify({'imagen_url': imagen_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

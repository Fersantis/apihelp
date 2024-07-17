from flask import Flask, request, jsonify, current_app
from app import app, mysql
from .models import fetch_all_tools, fetch_tools_by_code, insert_tools, fetch_all_usuario, fetch_usuario_by_credentials, comprar_herramienta
from flask_cors import CORS
import requests
import mercadopago

def init_routes(app):
    # Aquí van las rutas y sus respectivas funciones
    pass

CORS(app, resources={r"/*": {"origins": "http://localhost:8100"}})

# Configurar Mercado Pago
sdk = mercadopago.SDK("TEST-6482890036916762-071613-1755725f7a0536227a724bdb5c053082-1087871581")

@app.route('/tools', methods=['GET'])
def get_tools():
    tools = fetch_all_tools()
    return jsonify(tools)

@app.route('/usuario', methods=['GET'])
def get_usuario():
    usuarios = fetch_all_usuario()
    return jsonify(usuarios)

@app.route('/test', methods=['GET'])
def get_test():
    return jsonify("id:10")

@app.route('/tools/<code>', methods=['GET'])
def get_tool(code):
    tool = fetch_tools_by_code(code)
    return jsonify(tool)

@app.route('/tool', methods=['POST'])
def create_tools():
    tools_data = request.get_json()
    insert_tools(tools_data)
    return jsonify({'message': 'Herramienta creada exitosamente'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre = data.get('username')
    contrasena = data.get('password')

    user = fetch_usuario_by_credentials(nombre, contrasena)
    if user:
        response = {
            'nombre': user['nombre'],
            'contrasena': user['contrasena'],
            'correo': user['correo']
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Usuario no encontrado o credenciales inválidas'}), 401

@app.route('/CambioMoneda', methods=['GET'])
def CambioMoneda():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({"error": "Codigo no proporcionado"}), 400

    # Aquí deberías agregar la lógica para manejar el código y retornar la respuesta adecuada
    # Simulando una respuesta para fines de prueba:
    if codigo == "F073.TCO.PRE.Z.D":
        return jsonify({"cambio": 1.23})
    else:
        return jsonify({"error": "Codigo no encontrado"}), 404

@app.route('/create_preference', methods=['POST'])
def create_preference():
    data = request.get_json()
    preference_data = {
        "items": [
            {
                "title": data.get('title', 'Producto de prueba'),
                "quantity": int(data.get('quantity', 1)),
                "currency_id": data.get('currency_id', 'CLP'),
                "unit_price": float(data.get('unit_price', 100.0))
            }
        ],
        "back_urls": {
            "success": "http://localhost:8100/exito",
            "failure": "http://localhost:8100/fallido"
        },
        "auto_return": "approved"
    }
    preference_response = sdk.preference().create(preference_data)
    return jsonify(preference_response)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('username')
    contrasena = data.get('password')
    correo = data.get('correo')

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO usuario (nombre, contrasena, correo) VALUES (%s, %s, %s)", (nombre, contrasena, correo))
        mysql.connection.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error registrando usuario: {e}")
        return jsonify({'error': 'Error registrando usuario'}), 500
    finally:
        cursor.close()

@app.route('/comprar_herramienta', methods=['POST'])
def comprar_herramienta():
    try:
        data = request.json
        # Aquí procesa los datos recibidos
        # Por ejemplo, puedes acceder a los datos así: nombre = data['nombre']
        
        # Realiza la lógica de compra o actualización en la base de datos
        
        # Devuelve una respuesta exitosa
        return jsonify({'message': 'Compra realizada exitosamente'}), 200
    
    except Exception as e:
        # Si ocurre un error, maneja la excepción
        print(f"Error al procesar la compra: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

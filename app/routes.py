from flask import request, jsonify
from models import fetch_all_tools, fetch_tools_by_code, insert_tools, fetch_all_usuario

def init_routes(app):

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
        return jsonify({'message': 'Herramienta creado exitosamente'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Aquí deberías tener la lógica para verificar el username y password
        if username == 'correctUsername' and password == 'correctPassword':
            response = {
                'correo': username,
                'contrasena': password,
                'rol': 'user'  # rol puede ser un valor que definas
            }
            return jsonify([response])
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

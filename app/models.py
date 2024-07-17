from app import mysql
from flask import current_app

def fetch_all_tools():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM tools")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data
    except Exception as e:
        current_app.logger.error(f"Error fetching tools: {e}")
        return []
    finally:
        cursor.close()

def fetch_tools_by_code(code):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM tools WHERE code=%s", (code,))
        data = cursor.fetchone()
        return data
    except Exception as e:
        current_app.logger.error(f"Error fetching tool by code {code}: {e}")
        return None
    finally:
        cursor.close()

def insert_tools(tools_data):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO tools (code, name, price, category) VALUES (%s, %s, %s, %s)",
                       (tools_data['code'], tools_data['name'], tools_data['price'], tools_data['category']))
        mysql.connection.commit()
        return True
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error inserting tool: {e}")
        return False
    finally:
        cursor.close()

def fetch_all_usuario():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, nombre, contrasena, correo FROM usuario")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data
    except Exception as e:
        current_app.logger.error(f"Error fetching usuario: {e}")
        return []
    finally:
        cursor.close()

def fetch_usuario_by_credentials(nombre, contrasena):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, nombre, contrasena, correo FROM usuario WHERE nombre=%s AND contrasena=%s", (nombre, contrasena))
        data = cursor.fetchone()
        if data:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, data))
        return None
    except Exception as e:
        current_app.logger.error(f"Error fetching usuario by credentials: {e}")
        return None
    finally:
        cursor.close()

def insert_usuario(nombre, contrasena, correo):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO usuario (nombre, contrasena, correo) VALUES (%s, %s, %s)", (nombre, contrasena, correo))
        mysql.connection.commit()
        return True
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error inserting usuario: {e}")
        return False
    finally:
        cursor.close()

def comprar_herramienta(tool_id, cantidad):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT stock FROM tools WHERE id=%s", (tool_id,))
        stock = cursor.fetchone()
        if stock and stock['stock'] >= cantidad:
            new_stock = stock['stock'] - cantidad
            cursor.execute("UPDATE tools SET stock=%s WHERE id=%s", (new_stock, tool_id))
            mysql.connection.commit()
            return True, new_stock
        else:
            return False, "Stock insuficiente o herramienta no encontrada"
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error updating tool stock: {e}")
        return False, str(e)
    finally:
        cursor.close()


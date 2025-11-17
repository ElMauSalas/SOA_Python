#API REST CON PYTHON
#MAURCIO PÉREZ SALAS Y MARCO ANTONIO LAGUNES MONTERO
#7mo A.

from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)

# ===========================================================
#              MÓDULO 4: USUARIOS (REST)
# ===========================================================

# GET /usuarios  -> Lista todos los usuarios
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(usuarios)

# GET /usuarios/<id>  
@app.route("/usuarios/<int:id_usuario>", methods=["GET"])
def obtener_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify(usuario)



# POST /usuarios  -> Crea un usuario nuevo
@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()

    nombre    = data.get("nombre")
    apellidos = data.get("apellidos")
    email     = data.get("email")
    telefono  = data.get("telefono")
    genero    = data.get("genero")

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO usuarios (nombre, apellidos, email, telefono, genero)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (nombre, apellidos, email, telefono, genero)

    cursor.execute(sql, valores)
    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario creado", "id_usuario": nuevo_id}), 201


# PUT /usuarios/<id>  -> Actualiza un usuario existente
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):
    data = request.get_json()

    nombre    = data.get("nombre")
    apellidos = data.get("apellidos")
    email     = data.get("email")
    telefono  = data.get("telefono")
    genero    = data.get("genero")

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE usuarios
        SET nombre = %s,
            apellidos = %s,
            email = %s,
            telefono = %s,
            genero = %s
        WHERE id_usuario = %s
    """
    valores = (nombre, apellidos, email, telefono, genero, id_usuario)

    cursor.execute(sql, valores)
    conn.commit()

    filas = cursor.rowcount  # cuántos registros se actualizaron

    cursor.close()
    conn.close()

    if filas == 0:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado"})


# DELETE /usuarios/<id>  
@app.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id_usuario,))
    conn.commit()

    filas = cursor.rowcount

    cursor.close()
    conn.close()

    if filas == 0:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario eliminado"})

# ===========================================================
#                    ARRANCAR EL SERVIDOR
# ===========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

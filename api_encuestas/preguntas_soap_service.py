# preguntas_soap_service.py
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from db import get_connection


# ===================== MODELO SOAP =====================

class Pregunta(ComplexModel):
    id_pregunta  = Integer
    id_encuesta  = Integer
    text_pregunta = Unicode


# ===================== SERVICIO SOAP =====================

class PreguntasService(ServiceBase):

    # LISTAR TODAS LAS PREGUNTAS
    @rpc(_returns=Iterable(Pregunta))
    def listar_preguntas(ctx):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM preguntas")
        filas = cursor.fetchall()

        cursor.close()
        conn.close()

        for fila in filas:
            yield Pregunta(
                id_pregunta=fila["id_pregunta"],
                id_encuesta=fila["id_encuesta"],
                text_pregunta=fila["text_pregunta"]
            )

    # OBTENER PREGUNTA POR ID
    @rpc(Integer, _returns=Pregunta)
    def obtener_pregunta(ctx, id_pregunta):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM preguntas WHERE id_pregunta = %s",
            (id_pregunta,)
        )
        fila = cursor.fetchone()

        cursor.close()
        conn.close()

        if fila is None:
            # si no existe, regresamos una pregunta vacía o con id -1
            return Pregunta(
                id_pregunta=-1,
                id_encuesta=0,
                text_pregunta="NO_ENCONTRADA"
            )

        return Pregunta(
            id_pregunta=fila["id_pregunta"],
            id_encuesta=fila["id_encuesta"],
            text_pregunta=fila["text_pregunta"]
        )

    # CREAR PREGUNTA
    @rpc(Integer, Unicode, _returns=Integer)
    def crear_pregunta(ctx, id_encuesta, text_pregunta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO preguntas (id_encuesta, text_pregunta)
            VALUES (%s, %s)
        """
        valores = (id_encuesta, text_pregunta)

        cursor.execute(sql, valores)
        conn.commit()

        nuevo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        # regresamos el id generado
        return nuevo_id

    # ACTUALIZAR PREGUNTA
    @rpc(Integer, Integer, Unicode, _returns=Unicode)
    def actualizar_pregunta(ctx, id_pregunta, id_encuesta, text_pregunta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE preguntas
            SET id_encuesta = %s,
                text_pregunta = %s
            WHERE id_pregunta = %s
        """
        valores = (id_encuesta, text_pregunta, id_pregunta)

        cursor.execute(sql, valores)
        conn.commit()

        filas = cursor.rowcount

        cursor.close()
        conn.close()

        if filas == 0:
            return "Pregunta no encontrada"
        return "Pregunta actualizada"

    # ELIMINAR PREGUNTA
    @rpc(Integer, _returns=Unicode)
    def eliminar_pregunta(ctx, id_pregunta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM preguntas WHERE id_pregunta = %s"
        cursor.execute(sql, (id_pregunta,))
        conn.commit()

        filas = cursor.rowcount

        cursor.close()
        conn.close()

        if filas == 0:
            return "Pregunta no encontrada"
        return "Pregunta eliminada"


# ================== CONFIGURAR APLICACIÓN SOAP ==================

application = Application(
    [PreguntasService],
    'urn:preguntas.soap',        # namespace
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    servidor = make_server('0.0.0.0', 8000, wsgi_app)
    print("Servicio SOAP Preguntas corriendo en http://localhost:8000")
    print("WSDL en: http://localhost:8000/?wsdl")
    servidor.serve_forever()

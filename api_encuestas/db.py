import mysql.connector

def get_connection():

    conn = mysql.connector.connect(
        host="localhost",        
        user="root",
        password="]C|6pE6}u30Y6d>1d$8VIv5R£r#<P9",
        database="encuestas_db"
    )
    return conn

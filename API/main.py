
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from sqlalchemy import create_engine, text

load_dotenv()

app = FastAPI(
    title="OrderPulse API",
    description="API para consultar pedidos y carritos abandonados",
    version="1.0.0"
)

# Conexión con MySQL.
mysql_url = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DATABASE')}"
)
engine = create_engine(mysql_url)

# Conexión con MongoDB.
mongo_uri = (
    f"mongodb://{os.getenv('MONGO_USER')}:"
    f"{os.getenv('MONGO_PASSWORD')}@"
    f"{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"
    "?authSource=admin"
)
mongo_client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=5000
)
mongo_db = mongo_client[os.getenv("MONGO_DATABASE")]


@app.get("/")
def inicio():
    return {
        "proyecto": "OrderPulse",
        "mensaje": "API funcionando correctamente"
    }


@app.get("/health")
def comprobar_conexiones():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        mongo_client.admin.command("ping")

        return {
            "api": "ok",
            "mysql": "conectado",
            "mongodb": "conectado"
        }
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"Error de conexión: {str(error)}"
        )

# Hace que los análisis puedan consultarse mediante direcciones HTTP.
@app.get("/orders")
def consultar_pedidos():
    try:
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT id, customer_id, status, total, created_at
                FROM orders
                ORDER BY id
            """))

            return [dict(fila) for fila in resultado.mappings()]
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/abandoned-carts")
def consultar_carritos_abandonados():
    try:
        carritos = mongo_db.carts.find(
            {"status": "abandoned"},
            {"_id": 0}
        )

        return list(carritos)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

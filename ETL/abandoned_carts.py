# función que consulta MongoDB e identifica los carritos con estado abandoned. 
# Esta será la primera versión del análisis de OrderPulse.


import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Construye la dirección de conexión de MongoDB.
mongo_uri = (
    f"mongodb://{os.getenv('MONGO_USER')}:"
    f"{os.getenv('MONGO_PASSWORD')}@"
    f"{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"
    "?authSource=admin"
)

client = MongoClient(mongo_uri)
db = client[os.getenv("MONGO_DATABASE")]

try:
    # Busca únicamente los carritos cuyo estado es abandoned.
    carritos_abandonados = db.carts.find(
        {"status": "abandoned"}
    )

    total = 0

    print("REPORTE DE CARRITOS ABANDONADOS")
    print("-" * 40)

    for carrito in carritos_abandonados:
        total += 1

        print("Carrito:", carrito["cart_id"])
        print("Cliente:", carrito["customer_id"])
        print("Última actividad:", carrito["last_activity"])
        print("Productos:", len(carrito["items"]))
        print("-" * 40)

    print("Total de carritos abandonados:", total)

except Exception as error:
    print("Error al analizar los carritos:", error)

finally:
    client.close()

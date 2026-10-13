# va a generar carritos con distintos estados para que después 
# podamos identificar cuáles fueron abandonados y analizar su actividad.


import os
import random
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine, text

load_dotenv()

# Conecta con MySQL para obtener los clientes y pedidos existentes.
mysql_url = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DATABASE')}"
)

engine = create_engine(mysql_url)

# Conecta con MongoDB usando las credenciales del archivo .env.
mongo_uri = (
    f"mongodb://{os.getenv('MONGO_USER')}:"
    f"{os.getenv('MONGO_PASSWORD')}@"
    f"{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"
    "?authSource=admin"
)

client = MongoClient(mongo_uri)
db = client[os.getenv("MONGO_DATABASE")]

try:
    # Obtiene los identificadores que ya existen en MySQL.
    with engine.connect() as connection:
        clientes = connection.execute(
            text("SELECT id FROM customers")
        ).scalars().all()

        pedidos = connection.execute(
            text("SELECT id, customer_id FROM orders")
        ).mappings().all()

    if not clientes or not pedidos:
        raise ValueError(
            "Primero debes generar clientes y pedidos en MySQL."
        )

    # Evita duplicar los datos si el generador ya se ejecutó.
    if db.carts.count_documents({}) > 0:
        print("Ya existen carritos. No se insertaron duplicados.")
    else:
        estados = ["abandoned", "converted", "active"]
        tipos_evento = [
            "product_view",
            "add_to_cart",
            "checkout_started",
            "cart_abandoned"
        ]

        carritos = []
        eventos = []
        ahora = datetime.now(timezone.utc)

        # Genera 30 carritos con actividad ficticia.
        for numero in range(1, 31):
            cliente_id = random.choice(clientes)
            estado = random.choices(
                estados,
                weights=[50, 30, 20],
                k=1
            )[0]

            # El carrito contiene entre uno y tres productos ficticios.
            items = [
                {
                    "product_id": random.randint(1, 30),
                    "quantity": random.randint(1, 3)
                }
                for _ in range(random.randint(1, 3))
            ]

            creado = ahora - timedelta(
                hours=random.randint(1, 120)
            )
            ultima_actividad = creado + timedelta(
                minutes=random.randint(5, 180)
            )

            carrito = {
                "cart_id": f"CART-{numero:04}",
                "customer_id": cliente_id,
                "status": estado,
                "items": items,
                "created_at": creado,
                "last_activity": ultima_actividad
            }
            carritos.append(carrito)

            # Registra eventos relacionados con el carrito.
            eventos_carrito = ["product_view", "add_to_cart"]

            if estado == "converted":
                eventos_carrito.append("checkout_started")
            elif estado == "abandoned":
                eventos_carrito.append("cart_abandoned")

            for tipo in eventos_carrito:
                eventos.append({
                    "cart_id": carrito["cart_id"],
                    "customer_id": cliente_id,
                    "order_id": None,
                    "type": tipo,
                    "ts": ultima_actividad,
                    "payload": {
                        "status": estado
                    }
                })

        # Inserta los carritos y sus eventos en MongoDB.
        db.carts.insert_many(carritos)
        db.tracking_events.insert_many(eventos)

        print("¡Datos de MongoDB generados correctamente!")
        print("Carritos insertados:", len(carritos))
        print("Eventos insertados:", len(eventos))

        # Muestra cuántos carritos quedaron en cada estado.
        for estado in estados:
            cantidad = db.carts.count_documents(
                {"status": estado}
            )
            print(f"Carritos {estado}: {cantidad}")

except Exception as error:
    print("Error al generar datos en MongoDB:", error)

finally:
    engine.dispose()
    client.close()

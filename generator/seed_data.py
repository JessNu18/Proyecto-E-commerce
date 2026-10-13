# Este primer generador creará clientes, categorías y productos en MySQL. 
# Más adelante lo ampliaremos para generar pedidos, pagos, envíos y carritos.


import os
import random

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine, text

# Carga las variables de conexión desde el archivo .env.
load_dotenv()
fake = Faker("es_MX")

# Construye la conexión con MySQL.
mysql_url = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:"
    f"{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DATABASE')}"
)

engine = create_engine(mysql_url)

try:
    with engine.begin() as connection:
        # Comprueba si ya existen clientes para evitar duplicarlos.
        total = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar_one()

        if total > 0:
            print("Ya existen clientes. No se insertaron duplicados.")
        else:
            # Inserta 20 clientes ficticios.
            for _ in range(20):
                connection.execute(
                    text("""
                        INSERT INTO customers (email, nombre, ciudad)
                        VALUES (:email, :nombre, :ciudad)
                    """),
                    {
                        "email": fake.unique.email(),
                        "nombre": fake.name(),
                        "ciudad": fake.city()
                    }
                )

            # Crea las categorías del catálogo.
            categorias = [
                "Electrónica",
                "Ropa",
                "Hogar",
                "Deportes",
                "Libros"
            ]

            for categoria in categorias:
                connection.execute(
                    text("""
                        INSERT INTO categories (nombre)
                        VALUES (:nombre)
                    """),
                    {"nombre": categoria}
                )

            # Obtiene los identificadores de las categorías.
            categorias_db = connection.execute(
                text("SELECT id FROM categories")
            ).scalars().all()

            # Genera 30 productos con precio y stock aleatorios.
            for i in range(30):
                connection.execute(
                    text("""
                        INSERT INTO products
                            (sku, nombre, precio, stock, category_id)
                        VALUES
                            (:sku, :nombre, :precio, :stock, :category_id)
                    """),
                    {
                        "sku": f"PROD-{i + 1:03}",
                        "nombre": fake.catch_phrase(),
                        "precio": round(random.uniform(50, 2500), 2),
                        "stock": random.randint(0, 100),
                        "category_id": random.choice(categorias_db)
                    }
                )

            print("Datos iniciales insertados correctamente.")
            print("Clientes: 20")
            print("Categorías: 5")
            print("Productos: 30")

except Exception as error:
    print("Error al generar los datos:", error)

finally:
    engine.dispose()

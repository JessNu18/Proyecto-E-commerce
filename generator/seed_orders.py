# Crear pedidos automaticamente

import random

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Conecta el programa con MySQL usando las variables de .env.
url = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DATABASE')}"
)

engine = create_engine(url)

estados = ["pending", "paid", "processing", "shipped", "delivered"]

try:
    with engine.begin() as connection:
        # Evita generar pedidos duplicados al ejecutar el archivo otra vez.
        existentes = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        ).scalar_one()

        if existentes > 0:
            print("Ya existen pedidos. No se generaron duplicados.")
        else:
            clientes = connection.execute(
                text("SELECT id FROM customers")
            ).scalars().all()

            productos = connection.execute(
                text("SELECT id, precio FROM products")
            ).mappings().all()

            if not clientes or not productos:
                raise ValueError(
                    "Primero debes generar clientes y productos."
                )

            # Genera 40 pedidos con entre 1 y 4 productos cada uno.
            for _ in range(40):
                cliente_id = random.choice(clientes)
                estado = random.choice(estados)

                resultado = connection.execute(
                    text("""
                        INSERT INTO orders (customer_id, status, total)
                        VALUES (:cliente, :estado, 0)
                    """),
                    {
                        "cliente": cliente_id,
                        "estado": estado
                    }
                )

                pedido_id = resultado.lastrowid
                total = 0

                cantidad_productos = random.randint(1, 4)
                seleccionados = random.sample(
                    list(productos),
                    min(cantidad_productos, len(productos))
                )

                # Inserta los productos que forman parte del pedido.
                for producto in seleccionados:
                    cantidad = random.randint(1, 3)
                    precio = float(producto["precio"])
                    subtotal = cantidad * precio
                    total += subtotal

                    connection.execute(
                        text("""
                            INSERT INTO order_items
                                (order_id, product_id, cantidad,
                                 precio_unitario)
                            VALUES
                                (:pedido, :producto, :cantidad, :precio)
                        """),
                        {
                            "pedido": pedido_id,
                            "producto": producto["id"],
                            "cantidad": cantidad,
                            "precio": precio
                        }
                    )

                # Actualiza el total con la suma de los productos.
                connection.execute(
                    text("UPDATE orders SET total = :total WHERE id = :id"),
                    {"total": round(total, 2), "id": pedido_id}
                )

                # Registra un pago para cada pedido.
                pago_estado = "paid" if estado != "pending" else "pending"
                fecha_pago = (
                    text("CURRENT_TIMESTAMP") if False else None
                )

                connection.execute(
                    text("""
                        INSERT INTO payments
                            (order_id, metodo, monto, status, paid_at)
                        VALUES
                            (:pedido, :metodo, :monto, :estado,
                             CASE WHEN :estado = 'paid'
                                  THEN CURRENT_TIMESTAMP ELSE NULL END)
                    """),
                    {
                        "pedido": pedido_id,
                        "metodo": random.choice(
                            ["tarjeta", "transferencia", "paypal"]
                        ),
                        "monto": round(total, 2),
                        "estado": pago_estado
                    }
                )

                # Solo los pedidos enviados o entregados tienen envío.
                if estado in ["shipped", "delivered"]:
                    connection.execute(
                        text("""
                            INSERT INTO shipments
                                (order_id, carrier, tracking_number, status)
                            VALUES
                                (:pedido, :carrier, :tracking, :estado)
                        """),
                        {
                            "pedido": pedido_id,
                            "carrier": random.choice(
                                ["DHL", "FedEx", "Estafeta"]
                            ),
                            "tracking": f"OP-{pedido_id:06}",
                            "estado": estado
                        }
                    )

            print("¡Pedidos generados correctamente!")
            print("Pedidos: 40")
            print("Cada pedido incluye sus productos y un registro de pago.")
            print("Los pedidos enviados o entregados incluyen envío.")

except Exception as error:
    print("Error al generar pedidos:", error)

finally:
    engine.dispose()

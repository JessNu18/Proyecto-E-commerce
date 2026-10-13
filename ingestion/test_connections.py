import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient

# Carga las variables guardadas en el archivo .env
load_dotenv()

# Obtiene los datos de conexión de MySQL
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")

# Obtiene los datos de conexión de MongoDB
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_database = os.getenv("MONGO_DATABASE")
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")

# Construye la conexión con MySQL
mysql_url = (
    f"mysql+pymysql://{mysql_user}:{mysql_password}"
    f"@{mysql_host}:{mysql_port}/{mysql_database}"
)

# Crea el motor de conexión de SQLAlchemy
engine = create_engine(mysql_url)

# Comprueba que MySQL responda
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        print("MySQL conectado:", result.scalar())
except Exception as error:
    print("Error al conectar con MySQL:", error)
finally:
    engine.dispose()

# Construye la dirección de conexión de MongoDB
mongo_uri = (
    f"mongodb://{mongo_user}:{mongo_password}"
    f"@{mongo_host}:{mongo_port}/"
    "?authSource=admin"
)

# Crea el cliente de MongoDB
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

# Comprueba que MongoDB responda
try:
    client.admin.command("ping")
    print("MongoDB conectado:", mongo_database)
except Exception as error:
    print("Error al conectar con MongoDB:", error)
finally:
    client.close()

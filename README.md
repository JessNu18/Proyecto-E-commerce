# Proyecto-E-commerce
OrderPulse: rastreo de pedidos y análisis de carritos abandonados

# OrderPulse

Sistema de análisis de pedidos y carritos abandonados para un comercio electrónico. El proyecto utiliza MySQL para almacenar los datos transaccionales, MongoDB para registrar carritos y eventos de seguimiento, Python para generar y analizar datos, y FastAPI para exponer los resultados mediante una API REST.

## Objetivos

- Administrar clientes, categorías, productos, pedidos, pagos y envíos.
- Registrar carritos de compra y eventos de navegación.
- Identificar carritos marcados como abandonados.
- Obtener estadísticas de pedidos y ventas.
- Consultar la información mediante una API.
- Verificar el funcionamiento con pruebas automatizadas.

## Tecnologías utilizadas

- Python
- MySQL 8.4
- MongoDB 8
- Docker y Docker Compose
- FastAPI y Uvicorn
- SQLAlchemy y PyMySQL
- PyMongo
- Pandas y Faker
- Pytest y HTTPX

## Estructura del proyecto

```text
Proyecto-E-commerce/
├── API/
│   └── main.py
├── docs/
├── ETL/
│   └── abandoned_carts.py
├── generator/
│   ├── seed_data.py
│   ├── seed_orders.py
│   └── seed_mongo.py
├── ingestion/
│   └── test_connections.py
├── mongoDB/
│   └── init_collections.js
├── sql/
│   ├── 01_schema.sql
│   ├── 02_indexes.sql
│   └── 03_analytics_queries.sql
├── test/
│   └── test_api.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requisitos previos

- Python instalado y disponible desde la terminal.
- Docker y Docker Compose.
- Git.
- Acceso a una terminal de Codespaces o un entorno compatible.

## Instalación y configuración

### 1. Instalar dependencias

Desde la raíz del repositorio, ejecutar:

```bash
python -m pip install -r requirements.txt
```

### 2. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example` y configurar las credenciales de MySQL y MongoDB.

El archivo `.env` debe permanecer fuera del control de versiones porque contiene credenciales. No publicar contraseñas reales en GitHub.

### 3. Iniciar las bases de datos

```bash
docker compose up -d
```

Comprobar el estado de los servicios:

```bash
docker compose ps
```

MySQL debe llegar al estado `healthy` y MongoDB debe permanecer activo.

### 4. Preparar el esquema de MySQL

Los scripts SQL de la carpeta `sql/` definen las tablas, los índices y las consultas analíticas.

Si el esquema aún no existe, ejecutar:

```bash
docker exec -e MYSQL_PWD=orderpulse_dev_123 -i orderpulse-mysql mysql -u orderpulse orderpulse < sql/01_schema.sql
```

Después, crear los índices:

```bash
docker exec -e MYSQL_PWD=orderpulse_dev_123 -i orderpulse-mysql mysql -u orderpulse orderpulse < sql/02_indexes.sql
```

Si se cambian las credenciales locales, actualizar los comandos para que coincidan con la configuración del entorno.

### 5. Inicializar las colecciones de MongoDB

Si las colecciones aún no existen, ejecutar:

```bash
docker exec -i orderpulse-mongodb mongosh -u root -p mongo_dev_123 --authenticationDatabase admin --file /dev/stdin < mongoDB/init_collections.js
```

Este script crea las colecciones y sus índices iniciales.

### 6. Generar datos de prueba

Desde la raíz del proyecto, ejecutar los generadores en este orden:

```bash
python generator/seed_data.py
python generator/seed_orders.py
python generator/seed_mongo.py
```

Los programas generan datos ficticios para probar las consultas y los análisis. Los generadores comprueban la existencia de datos para evitar algunas inserciones duplicadas; si se necesita repetir la carga, revisar primero el contenido de las bases de datos.

### 7. Verificar las conexiones

```bash
python ingestion/test_connections.py
```

El resultado esperado es que MySQL y MongoDB aparezcan como conectados.

## Ejecución del análisis ETL

Para consultar los carritos cuyo estado está marcado como `abandoned`:

```bash
python ETL/abandoned_carts.py
```

El programa muestra el identificador del carrito, el cliente, la última actividad y el número de productos.

## Ejecutar las consultas analíticas

```bash
docker exec -e MYSQL_PWD=orderpulse_dev_123 -i orderpulse-mysql mysql -u orderpulse orderpulse < sql/03_analytics_queries.sql
```

Las consultas permiten analizar los pedidos por estado, las ventas de pagos completados, los clientes con más pedidos y los productos más vendidos.

## Ejecutar la API

Desde la raíz del proyecto:

```bash
python -m uvicorn main:app --app-dir API --reload --host 0.0.0.0 --port 8000
```

La API expone los siguientes endpoints:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Información básica de la API. |
| GET | `/health` | Comprueba las conexiones con MySQL y MongoDB. |
| GET | `/orders` | Consulta los pedidos. |
| GET | `/abandoned-carts` | Consulta los carritos marcados como abandonados. |

En GitHub Codespaces, abrir el puerto `8000` desde la pestaña **Ports**. Después, acceder a `/docs` al final de la URL de la aplicación para consultar la documentación interactiva de FastAPI.

## Ejecutar las pruebas automatizadas

```bash
python -m pytest test/test_api.py -v
```

Las pruebas verifican la respuesta inicial de la API, las conexiones con las bases de datos, la consulta de pedidos y la consulta de carritos abandonados.

## Seguridad

- No subir el archivo `.env` a GitHub.
- Utilizar `.env.example` para documentar los nombres de las variables necesarias, sin incluir contraseñas reales.
- Las credenciales de los ejemplos son exclusivamente para desarrollo local.
- No utilizar estas credenciales ni datos ficticios en un entorno de producción.

## Estado actual

El proyecto cuenta con bases de datos MySQL y MongoDB, generación de datos de prueba, análisis inicial de carritos abandonados, consultas SQL, endpoints de FastAPI y pruebas automatizadas.

Las pruebas de API se ejecutaron correctamente: **4 pruebas aprobadas** en el entorno de desarrollo utilizado.

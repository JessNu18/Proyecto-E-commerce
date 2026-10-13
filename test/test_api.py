from fastapi.testclient import TestClient

from API.main import app

# Permite probar la API sin abrir un navegador.
client = TestClient(app)


def test_inicio():
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert respuesta.json()["proyecto"] == "OrderPulse"


def test_health():
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    datos = respuesta.json()

    assert datos["mysql"] == "conectado"
    assert datos["mongodb"] == "conectado"


def test_consultar_pedidos():
    respuesta = client.get("/orders")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    assert len(respuesta.json()) > 0


def test_carritos_abandonados():
    respuesta = client.get("/abandoned-carts")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

    # Comprueba que todos los resultados estén abandonados.
    for carrito in respuesta.json():
        assert carrito["status"] == "abandoned"

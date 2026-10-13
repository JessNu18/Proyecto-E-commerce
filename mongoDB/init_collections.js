// Este archivo contendrá instrucciones para preparar las colecciones de nuestra aplicación.

//selecciona la base de datos orderpulse en MongoDB.
db = db.getSiblingDB("orderpulse");

//crea una colección para almacenar documentos.
db.createCollection("carts");
db.createCollection("tracking_events");

//crea índices para acelerar determinadas búsquedas.
db.carts.createIndex({
    customer_id: 1,
    status: 1
});

db.tracking_events.createIndex({
    order_id: 1,
    ts: 1
});

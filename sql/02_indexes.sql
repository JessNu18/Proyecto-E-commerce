USE orderpulse;

-- Indice para buscar pedidos de un cliente por fecha
-- Ayuda a consultar los pedidos de un cliente y ordenarlos o filtrarlos por fecha.
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at);

-- Indice para buscar pedidos por su estado
-- Ayuda a localizar pedidos según su estado, por ejemplo, pending, shipped o delivered.
CREATE INDEX idx_orders_status
ON orders (status);

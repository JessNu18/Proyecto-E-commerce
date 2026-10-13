-- Consultas que permiten analizar los pedidos, las ventas y el comportamiento de los clientes.
USE orderpulse;

-- 1. Cantidad de pedidos por estado.
SELECT
    status,
    COUNT(*) AS total_pedidos
FROM orders
GROUP BY status
ORDER BY total_pedidos DESC;

-- 2. Ventas totales de pedidos pagados.
SELECT
    SUM(monto) AS ventas_totales
FROM payments
WHERE status = 'paid';

-- 3. Los 5 clientes con más pedidos.
SELECT
    c.id,
    c.nombre,
    COUNT(o.id) AS total_pedidos
FROM customers AS c
JOIN orders AS o
    ON c.id = o.customer_id
GROUP BY c.id, c.nombre
ORDER BY total_pedidos DESC
LIMIT 5;

-- 4. Los 5 productos más vendidos por unidades.
SELECT
    p.nombre,
    SUM(oi.cantidad) AS unidades_vendidas
FROM order_items AS oi
JOIN products AS p
    ON oi.product_id = p.id
GROUP BY p.id, p.nombre
ORDER BY unidades_vendidas DESC
LIMIT 5;

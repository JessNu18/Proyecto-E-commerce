CREATE DATABASE IF NOT EXISTS orderpulse;
USE orderpulse;

-- 1. Clientes de la tienda
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Categorias de productos
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    parent_id INT,
    FOREIGN KEY (parent_id)
        REFERENCES categories(id)
        ON DELETE SET NULL
);

-- 3. Productos disponibles
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category_id INT,
    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE SET NULL,
    CHECK (precio >= 0),
    CHECK (stock >= 0)
);

-- 4. Pedidos de los clientes
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    total DECIMAL(12,2) NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    shipped_at DATETIME NULL,
    delivered_at DATETIME NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT,
    CHECK (total >= 0)
);

-- 5. Productos incluidos en cada pedido
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT,
    CHECK (cantidad > 0),
    CHECK (precio_unitario >= 0)
);

-- 6. Pagos de los pedidos
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    metodo VARCHAR(50) NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    paid_at DATETIME NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,
    CHECK (monto >= 0)
);

-- 7. Envios de los pedidos
CREATE TABLE IF NOT EXISTS shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    carrier VARCHAR(100) NOT NULL,
    tracking_number VARCHAR(100) UNIQUE,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
);

-- 8. Resultados diarios del embudo de conversion
-- Guarda resultados agregados por fecha, como:
-- visitas, carritos, checkouts, compras y tasa de abandono.
CREATE TABLE IF NOT EXISTS daily_funnel (
    fecha DATE PRIMARY KEY,
    visitas INT NOT NULL DEFAULT 0,
    carritos INT NOT NULL DEFAULT 0,
    checkouts INT NOT NULL DEFAULT 0,
    compras INT NOT NULL DEFAULT 0,
    tasa_abandono DECIMAL(5,2) NOT NULL DEFAULT 0,
    CHECK (visitas >= 0),
    CHECK (carritos >= 0),
    CHECK (checkouts >= 0),
    CHECK (compras >= 0),
    CHECK (tasa_abandono BETWEEN 0 AND 100)
);

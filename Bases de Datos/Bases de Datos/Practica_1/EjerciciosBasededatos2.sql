
CREATE DATABASE IF NOT EXISTS ventas;

USE ventas;

CREATE TABLE clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100)
);


CREATE TABLE productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10, 2) NOT NULL
);


CREATE TABLE facturas (
  id_factura INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha DATE NOT NULL,
  total DECIMAL(10, 2),
  FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

CREATE TABLE factura_productos (
  id_factura INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10, 2) NOT NULL,
  PRIMARY KEY (id_factura, id_producto),
  FOREIGN KEY (id_factura) REFERENCES facturas (id_factura),
  FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
);


INSERT INTO
  clientes (nombre, email)
VALUES
  ('Juan Pérez', 'juan.perez@email.com'),
  ('Ana Gómez', 'ana.gomez@email.com');

INSERT INTO
  productos (nombre, precio)
VALUES
  ('Laptop', 1200.00),
  ('Mouse', 25.00),
  ('Teclado', 45.00);

INSERT INTO
  facturas (id_cliente, fecha, total)
VALUES
  (1, '2024-06-01', 1270.00),
  (2, '2024-06-02', 70.00);

INSERT INTO
  factura_productos (
    id_factura,
    id_producto,
    cantidad,
    precio_unitario
  )
VALUES
  (1, 1, 1, 1200.00), -- Juan compra 1 Laptop
  (1, 2, 2, 25.00), -- Juan compra 2 Mouse
  (2, 3, 1, 45.00), -- Ana compra 1 Teclado
  (2, 2, 1, 25.00);


SELECT
  f.id_factura,
  c.nombre AS cliente,
  f.fecha,
  f.total
FROM
  facturas f
  JOIN clientes c ON f.id_cliente = c.id_cliente;


SELECT
  fp.id_factura,
  p.nombre AS producto,
  fp.cantidad,
  fp.precio_unitario
FROM
  factura_productos fp
  JOIN productos p ON fp.id_producto = p.id_producto
WHERE
  fp.id_factura = 1;


SELECT
  p.nombre,
  SUM(fp.cantidad) AS total_vendido
FROM
  factura_productos fp
  JOIN productos p ON fp.id_producto = p.id_producto
GROUP BY
  p.nombre;

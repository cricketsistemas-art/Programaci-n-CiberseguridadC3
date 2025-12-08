-- Crear la base de datos
CREATE DATABASE biblioteca;
USE biblioteca;

-- Crear la tabla de autores
CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50)
);

-- Crear la tabla de libros
CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    anio_publicacion INT,
    id_autor INT,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
);

-- Insertar autores de ejemplo
INSERT INTO autores (nombre, nacionalidad) VALUES
('Gabriel García Márquez', 'Colombiana'),
('Isabel Allende', 'Chilena'),
('Jorge Luis Borges', 'Argentina');

-- Insertar libros de ejemplo
INSERT INTO libros (titulo, anio_publicacion, id_autor) VALUES
('Cien años de soledad', 1967, 1),
('El amor en los tiempos del cólera', 1985, 1),
('La casa de los espíritus', 1982, 2),
('Fervor de Buenos Aires', 1923, 3);

-- Consultar todos los libros con su autor
SELECT l.titulo, l.anio_publicacion, a.nombre AS autor
FROM libros l
JOIN autores a ON l.id_autor = a.id_autor;

-- Consultar todos los autores y la cantidad de libros que han escrito
SELECT a.nombre, COUNT(l.id_libro) AS cantidad_libros
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
GROUP BY a.id_autor, a.nombre;
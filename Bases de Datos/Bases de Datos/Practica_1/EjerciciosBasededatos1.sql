-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS colegio;

USE colegio;

-- 2. Crear la tabla de estudiantes
CREATE TABLE estudiantes (
  id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  fecha_nacimiento DATE
);

-- 3. Crear la tabla de cursos
CREATE TABLE cursos (
  id_curso INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255)
);

-- 4. Crear la tabla de matriculas (relaciona estudiantes y cursos)
CREATE TABLE matriculas (
  id_matricula INT AUTO_INCREMENT PRIMARY KEY,
  id_estudiante INT NOT NULL,
  id_curso INT NOT NULL,
  fecha_matricula DATE NOT NULL,
  FOREIGN KEY (id_estudiante) REFERENCES estudiantes (id_estudiante),
  FOREIGN KEY (id_curso) REFERENCES cursos (id_curso)
);

-- 5. Insertar datos de ejemplo
INSERT INTO
  estudiantes (nombre, fecha_nacimiento)
VALUES
  ('Carlos López', '2005-03-15'),
  ('María Torres', '2006-07-22'),
  ('Lucía Fernández', '2005-11-30');

INSERT INTO
  cursos (nombre, descripcion)
VALUES
  ('Matemáticas', 'Curso de matemáticas básicas'),
  ('Historia', 'Curso de historia universal'),
  ('Inglés', 'Curso de inglés intermedio');

INSERT INTO
  matriculas (id_estudiante, id_curso, fecha_matricula)
VALUES
  (1, 1, '2024-06-01'),
  (1, 2, '2024-06-01'),
  (2, 1, '2024-06-02'),
  (3, 3, '2024-06-03');

-- 6. Consultas sencillas
-- a) Listar todos los estudiantes
SELECT
  *
FROM
  estudiantes;

-- b) Listar todos los cursos
SELECT
  *
FROM
  cursos;

-- c) Mostrar las matrículas con el nombre del estudiante y el nombre del curso
SELECT
  m.id_matricula,
  e.nombre AS estudiante,
  c.nombre AS curso,
  m.fecha_matricula
FROM
  matriculas m
  JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
  JOIN cursos c ON m.id_curso = c.id_curso;
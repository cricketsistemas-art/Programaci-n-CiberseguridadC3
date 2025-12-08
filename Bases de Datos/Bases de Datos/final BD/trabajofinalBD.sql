CREATE DATABASE gestion_academica;
USE gestion_academica;
CREATE TABLE Departamento (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE
);

CREATE TABLE Curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Clase (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT,
    id_profesor INT,
    periodo VARCHAR(20),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_profesor) REFERENCES Profesor(id_profesor)
);

CREATE TABLE Inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT,
    id_clase INT,
    fecha_inscripcion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante),
    FOREIGN KEY (id_clase) REFERENCES Clase(id_clase)
);

CREATE TABLE Calificacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT,
    nota DECIMAL(4,2),
    fecha DATE,
    FOREIGN KEY (id_inscripcion) REFERENCES Inscripcion(id_inscripcion)
);
-- consultas--
SELECT e.nombre AS estudiante, c.id_clase
FROM Estudiante e
JOIN Inscripcion i ON e.id_estudiante = i.id_estudiante
JOIN Clase c ON i.id_clase = c.id_clase
WHERE c.id_clase = 1;
-- consultas--
SELECT cu.nombre AS curso, AVG(ca.nota) AS promedio
FROM Calificacion ca
JOIN Inscripcion i ON ca.id_inscripcion = i.id_inscripcion
JOIN Clase cl ON i.id_clase = cl.id_clase
JOIN Curso cu ON cl.id_curso = cu.id_curso
GROUP BY cu.id_curso;
-- consultas y modificaciones-- 
INSERT INTO Estudiante (nombre, fecha_nacimiento)
VALUES ('Juan Pérez', '2002-05-10');
-- actualizaciones-- 
UPDATE Departamento
SET nombre = 'Ciencias Exactas'
WHERE id_departamento = 1;
-- modificaciones-- 
DELETE FROM Inscripcion
WHERE id_inscripcion = 10;
-- consultas con joins---
SELECT cu.nombre AS curso, COUNT(DISTINCT i.id_estudiante) AS total_estudiantes
FROM Curso cu
JOIN Clase cl ON cu.id_curso = cl.id_curso
JOIN Inscripcion i ON cl.id_clase = i.id_clase
GROUP BY cu.id_curso;





create database proyectoCine

CREATE TABLE Pelicula (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100),
    genero VARCHAR(50),
    duracion INT, -- en minutos
    clasificacion VARCHAR(10),
    idioma VARCHAR(50)
);

CREATE TABLE Sala (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    capacidad INT,
    tipo VARCHAR(50) -- 2D, 3D, IMAX, etc.
);

CREATE TABLE Funcion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pelicula_id INT,
    sala_id INT,
    fecha DATE,
    hora TIME,
    precio DECIMAL(6,2),
    FOREIGN KEY (pelicula_id) REFERENCES Pelicula(id),
    FOREIGN KEY (sala_id) REFERENCES Sala(id)
);

CREATE TABLE Cliente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE Boleto (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    funcion_id INT,
    cantidad INT,
    fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id),
    FOREIGN KEY (funcion_id) REFERENCES Funcion(id)
);


-- Vista de funciones disponibles con información completa
CREATE VIEW VistaFunciones AS
SELECT f.id, p.titulo, s.nombre AS sala, f.fecha, f.hora, f.precio
FROM Funcion f
JOIN Pelicula p ON f.pelicula_id = p.id
JOIN Sala s ON f.sala_id = s.id;

-- Vista de ingresos por película
CREATE VIEW IngresosPorPelicula AS
SELECT p.titulo, SUM(b.cantidad * f.precio) AS ingresos
FROM Boleto b
JOIN Funcion f ON b.funcion_id = f.id
JOIN Pelicula p ON f.pelicula_id = p.id
GROUP BY p.titulo;

-- Trigger para validar que la sala no se sobrellene
DELIMITER //
CREATE TRIGGER validar_capacidad
BEFORE INSERT ON Boleto
FOR EACH ROW
BEGIN
    DECLARE ocupados INT;
    DECLARE capacidad_sala INT;

    SELECT SUM(cantidad) INTO ocupados
    FROM Boleto
    WHERE funcion_id = NEW.funcion_id;

    SELECT s.capacidad INTO capacidad_sala
    FROM Funcion f JOIN Sala s ON f.sala_id = s.id
    WHERE f.id = NEW.funcion_id;

    IF ocupados + NEW.cantidad > capacidad_sala THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No hay suficientes asientos disponibles para esta función.';
    END IF;
END;
//
DELIMITER ;


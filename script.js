// Conectarse o crear la base de datos proyectoCineMongo
// use proyectoCineMongo; // Ejecutar esto primero en mongosh si no está en el script

// 1. Crear colecciones (opcional, se crean al primer insert)
db.createCollection("peliculas");
db.createCollection("salas");
db.createCollection("clientes");
db.createCollection("funciones");
db.createCollection("boletos");

// --- Insertar datos de ejemplo ---

// Películas
const pelicula1 = db.peliculas.insertOne({
    titulo: "El Origen",
    genero: "Ciencia Ficción",
    duracion: 148,
    clasificacion: "PG-13",
    idioma: "Inglés"
}).insertedId;

const pelicula2 = db.peliculas.insertOne({
    titulo: "Interestelar",
    genero: "Ciencia Ficción",
    duracion: 169,
    clasificacion: "PG-13",
    idioma: "Inglés"
}).insertedId;

// Salas
const sala1 = db.salas.insertOne({
    nombre: "Sala 1",
    capacidad: 100,
    tipo: "2D"
}).insertedId;

const sala2 = db.salas.insertOne({
    nombre: "Sala 4D Plus",
    capacidad: 70,
    tipo: "4D"
}).insertedId;

// Clientes
const cliente1 = db.clientes.insertOne({
    nombre: "Carlos Lopez",
    correo: "carlos.lopez@me.com",
    telefono: "3009876543"
}).insertedId;

// Funciones
// Usamos los IDs de las películas y salas insertadas arriba
const funcion1 = db.funciones.insertOne({
    pelicula_id: pelicula1, // Referencia a "El Origen"
    sala_id: sala1,         // Referencia a "Sala 1"
    fecha: new Date("2025-06-10"),
    hora: "18:00",
    precio: 10.00
}).insertedId;

const funcion2 = db.funciones.insertOne({
    pelicula_id: pelicula2, // Referencia a "Interestelar"
    sala_id: sala2,         // Referencia a "Sala 4D Plus"
    fecha: new Date("2025-06-10"),
    hora: "21:00",
    precio: 15.00
}).insertedId;

// Boletos
db.boletos.insertOne({
    cliente_id: cliente1,
    funcion_id: funcion1,
    cantidad: 2,
    fecha_compra: new Date() // Fecha y hora actual de la compra
});

db.boletos.insertOne({
    cliente_id: cliente1, // Mismo cliente, diferente función
    funcion_id: funcion2,
    cantidad: 4,
    fecha_compra: new Date()
});

// --- Verificación ---
print("Películas insertadas:", db.peliculas.countDocuments());
print("Salas insertadas:", db.salas.countDocuments());
print("Clientes insertados:", db.clientes.countDocuments());
print("Funciones insertadas:", db.funciones.countDocuments());
print("Boletos insertados:", db.boletos.countDocuments());

// Ejemplo de cómo se vería un boleto con sus referencias
printjson(db.boletos.findOne());
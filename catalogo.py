# Lista de diccionarios (Estructura profesional de datos)
inventario = [
    {"nombre": "Teclado", "precio": 50, "stock": 15},
    {"nombre": "Mouse", "precio": 25, "stock": 0},
    {"nombre": "Monitor", "precio": 200, "stock": 5},
    {"nombre": "Cable HDMI", "precio": 10, "stock": 100},
    {"nombre": "Mouse Pad", "precio": 15, "stock": 25},
    {"nombre": "Cable USB", "precio": 5, "stock": 50},
    {"nombre": "Cable VGA", "precio": 20, "stock": 0},
    {"nombre": "Cable DVI", "precio": 15, "stock": 20},
    {"nombre": "Cable USB-C", "precio": 25, "stock": 0},
    {"nombre": "Cable HDMI", "precio": 10, "stock": 100}, 
]

print("--- REPORTE DE INVENTARIO ---")

# Recorremos cada producto del inventario
for producto in inventario:
    nombre = producto["nombre"]
    stock = producto["stock"]
    
    if stock > 0:
        estado = "✅ Disponible"
    else:
        estado = "❌ Agotado"
        
    print(f"Producto: {nombre:12} | Estado: {estado} ({stock} unidades)")
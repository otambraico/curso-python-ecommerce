# Se define 3 variables para un artículo
nombre_articulo = "Teclado Mecánico"
precio_unitario = 50.5
stock_actual = 10  # Cambia este número para probar

print(f"--- Sistema de Inventario: {nombre_articulo} ---")

# Lógica de decisión
if stock_actual > 0:
    print("Estado: ✅ Producto disponible para la venta.")
    valor_total = precio_unitario * stock_actual
    print(f"Valor total en almacén: ${valor_total}")
else:
    print("Estado: ❌ Alerta: Producto agotado.")
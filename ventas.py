# Definir la "máquina"
def procesar_compra(producto, precio, cant, stock):
    if cant <= stock:
        total = precio * cant
        if total > 500:
            total = total * 0.90 # 10% de descuento
            return f"✅ Compra de {producto} exitosa, Total : ${total} con descuento" 
        else:
            return f"❌ No hay suficinte stock de {producto}."

# Usando la "máquina"
resultado = procesar_compra("Laptop", 1000, 10, 50)
print(resultado)
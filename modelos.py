# Definiendo nuestra Clase
class Producto:
    def __init__(self, nombre, precio, stock):
        # Atributos (Características)
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_info(self):
        return f"Producto: {self.nombre} | Precio: ${self.precio} | Stock: {self.stock}"

    def vender(self, cantidad):
        if cantidad <= self.stock:
            self.stock -= cantidad
            print(f"✅ Venta realizada: {cantidad} unidades de {self.nombre}")
        else:
            print(f"❌ Error: No hay suficiente stock de {self.nombre}")
    
    def reposicionar_stock(self, cantidad):
        self.stock += cantidad
        print(f"el stock actual es {self.stock}")

    def identificar(self):
        print(f"Midirección en memoria es: {self}")

# --- Probando nuestra Clase ---
laptop = Producto("MacBook Air", 1200, 5)
print(laptop.mostrar_info())

laptop.vender(2)
print(laptop.mostrar_info())

celular = Producto("iPhone", 800, 10)
print(celular.reposicionar_stock(5))

p1 = Producto("Teclado", 50, 10)
p2 = Producto("Mouse", 20, 5)

p1.identificar()
p2.identificar()
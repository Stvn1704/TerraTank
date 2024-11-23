
class Player:
    vida = 100
    daño = 10
    size = 180
    def __init__(self, nombre):
        self.nombre = nombre
    
    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            print(f"{self.nombre} ha muerto")
        else:
            print(f"{self.nombre} recibió {cantidad} de daño. Vida restante: {self.vida}")
    
    def curarse(self, cantidad):
        self.vida += cantidad
        print(f"{self.nombre} se curó {cantidad}. Vida actual: {self.vida}")




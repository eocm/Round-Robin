class Proceso:
    def __init__(self, id, operacion, tme, num1, num2, ttb=0):
        self.id = id
        self.operacion = operacion
        self.tme = tme
        self.num1 = num1
        self.num2 = num2
        self.error = 0
        self.ttb = ttb
        self.tt = 0
        self.tllegada = None
        self.tfinalizacion = None
        self.espera = None
        self.tretorno = None
        self.trespuesta = None
        self.tquantum = 0

    def __str__(self):
        return ( str(self.id) + " " + str(self.operacion)+ " " + str(self.tme) + " " + str(self.num1)  + " " +  str(self.num2))
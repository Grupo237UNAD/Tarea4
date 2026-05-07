# SISTEMA SOFTWARE FJ (POO + EXCEPCIONES)

# 1. IMPORTACIONES
# ------------------------------
from abc import ABC, abstractmethod
import datetime

# ------------------------------
# 2. ARCHIVO DE LOGS
# ------------------------------

def registrar_log(mensaje):
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{datetime.datetime.now()} - {mensaje}\n")

# ------------------------------
# 3. EXCEPCIONES PERSONALIZADAS
# ------------------------------

class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

# ------------------------------
# 4. CLASE ABSTRACTA BASE
# ------------------------------

class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

# ------------------------------
# 5. CLASE CLIENTE
# ------------------------------

class Cliente(Entidad):
    def __init__(self, nombre, identificacion):
        try:
            if not nombre or not identificacion:
                raise ErrorValidacion("Datos del cliente inválidos")

            self.__nombre = nombre
            self.__identificacion = identificacion
        except Exception as e:
            registrar_log(str(e))
            raise

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - ID: {self.__identificacion}"

# ------------------------------
# 6. CLASE ABSTRACTA SERVICIO
# ------------------------------

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ------------------------------
# 7. SERVICIOS ESPECÍFICOS
# ------------------------------

class Sala(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio_base * horas

    def descripcion(self):
        return "Reserva de sala"

class Equipo(Servicio):
    def calcular_costo(self, dias=1):
        return self.precio_base * dias

    def descripcion(self):
        return "Alquiler de equipo"

class Asesoria(Servicio):
    def calcular_costo(self, horas=1, descuento=0):
        costo = self.precio_base * horas
        return costo - (costo * descuento)

    def descripcion(self):
        return "Asesoría especializada"

# ------------------------------
# 8. CLASE RESERVA
# ------------------------------

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        try:
            if duracion <= 0:
                raise ErrorReserva("Duración inválida")

            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"

        except Exception as e:
            registrar_log(str(e))
            raise

    def confirmar(self):
        try:
            self.estado = "Confirmada"
        except Exception as e:
            registrar_log(str(e))

    def cancelar(self):
        try:
            self.estado = "Cancelada"
        except Exception as e:
            registrar_log(str(e))

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
            self.confirmar()
            return costo
        except Exception as e:
            registrar_log(str(e))
            raise ErrorReserva("Error al procesar reserva") from e

# ------------------------------
# 9. SIMULACIÓN (10 CASOS)
# ------------------------------

clientes = []
servicios = []
reservas = []

# CASOS
for i in range(10):
    try:
        # Crear cliente (uno inválido)
        if i == 3:
            c = Cliente("", "")
        else:
            c = Cliente(f"Cliente{i}", i)
        clientes.append(c)

        # Crear servicio
        if i % 3 == 0:
            s = Sala("Sala", 100)
        elif i % 3 == 1:
            s = Equipo("Equipo", 200)
        else:
            s = Asesoria("Asesoría", 300)

        servicios.append(s)

        # Crear reserva (una inválida)
        if i == 5:
            r = Reserva(c, s, -1)
        else:
            r = Reserva(c, s, i+1)

        reservas.append(r)

        # Procesar reserva
        costo = r.procesar()
        print(f"Reserva procesada - Costo: {costo}")

    except Exception as e:
        print(f"Error detectado: {e}")
        registrar_log(f"Error en simulación: {e}")

# ------------------------------
# FIN DEL SISTEMA

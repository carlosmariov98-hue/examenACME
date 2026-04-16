from csv import DictReader
from pathlib import Path


rutaBase = Path(__file__).parent.parent
ruta = rutaBase/"DB"


def esDigito(campo):
    return str(campo).isdigit()

def ivaValido(campo):
    return 1 <= campo <= 29

def validacionPuestos(campo):
    return 0 < campo <= 50

def campoNoNuloNiNegativo(campo):
    return campo > 0

def notBlank(campo):
    return campo.strip()


def validacionCampos(nombreCampo, tipo, condicion=None, mensajeCondicion=None):
    while(True):
        try:
            campo = tipo(input(f"{nombreCampo} -> "))

            if condicion and not condicion(campo):
                print(f"El campo ({nombreCampo.upper()}) {mensajeCondicion}")
                continue
            return campo
        
        except ValueError:
            print(f"El campo ({nombreCampo.upper()}) solo acepta números.")



def verificarExistencia(ruta, archivo):
    try:
        with open(ruta/archivo,"r",newline="",encoding="utf-8") as file:
            return list(DictReader(file))
    except FileNotFoundError:
        with open(ruta/archivo,"w",newline="",encoding="utf-8") as file:
            pass
        return []



def asignarCodigoFactura():
    listaFacturas = verificarExistencia(ruta,"Facturas.csv")

    if listaFacturas:
        codigo = int(listaFacturas[-1]["ID_FACTURA"])+1
    else:
        codigo = 1
    return codigo


def validacionEmail():
    while(True):
        texto = ""
        email = input("Correo electrónico -> ")
        if "@" in email:
            texto += email[email.find("@")+1:]
            if texto in ("gmail.com","hotmail.com","hotmail.es"):
                return email
        print("El correo electrónico no es válido o no está soportado por nuestros servidores. (Gmail o Hotmail)")


def guardarValidacion():
    while(True):
        respuesta = input("¿Quiere guardar la factura?").title()
        if respuesta in ("Si","Sí"):
            return True
        elif respuesta == "No":
            return False
        print("Opción inválida.")
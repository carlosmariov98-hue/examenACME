import App.Funciones as Funciones
from datetime import datetime

import App.Utilidades as Utilities

def crearProducto():
    opcion = ""
    print("Para la creación de un producto, necesitamos los siguientes datos:")
    while(opcion not in ("1","2","3")):
        print("El producto a añadir es:\n1.Bebida\n2.Platillo\n3.Postre")
        opcion = input("Opción -> ")
        match(opcion):
            case "1":
                tipoProducto = "Bebida"
            case "2":
                tipoProducto = "Platillo"
            case "3":
                tipoProducto = "Postre"
            case _:
                print("Opción inválida. Intente de nuevo.")

    
    codigo = Utilities.validacionCampos(nombreCampo='Código',tipo=int,condicion=Utilities.esDigito,mensajeCondicion='solo puede tener números.')

    nombre = Utilities.validacionCampos('Nombre',str,Utilities.notBlank,'no puede estar vacío.')

    valor = Utilities.validacionCampos('Valor',int,Utilities.campoNoNuloNiNegativo,'no puede ser nulo ni negativo.')
    
    iva = Utilities.validacionCampos('IVA',int,Utilities.ivaValido,'no puede ser menor que 1 ni mayor que 30.')
    
    mensaje = Funciones.crearProducto(codigo,tipoProducto,nombre,valor,iva)
    if mensaje:
        print(mensaje)
    else:
        print(f"El producto {nombre} se creó correctamente.")    


def crearMesa():
    print("Para crear una mesa, necesitamos los siguientes datos: ")

    codigo = Utilities.validacionCampos('Código',int,Utilities.esDigito,'solo puede tener números.')

    puestos = Utilities.validacionCampos('Cantidad de puestos',int,Utilities.validacionPuestos,'no puede ser menor que 1 ni mayor que 50.')
    
    if puestos > 0 and puestos <= 50:
        if puestos == 1:
            tipoMesa = "Individual"
        elif puestos == 2:
            tipoMesa = "Pareja"
        elif puestos >= 3 and puestos <= 16:
            tipoMesa = "Familiar"
        else:
            tipoMesa = "Corporación"

    mensaje = Funciones.crearMesa(codigo,tipoMesa,puestos)
    if mensaje:
        print(mensaje)
    else:
        print("Se creó la mesa correctamente.")

def crearCliente():
    print("Para crear un cliente, necesitamos los siguientes datos: ")

    idCliente = Utilities.validacionCampos('ID',int,Utilities.esDigito,'solo puede tener números.')

    nombre = Utilities.validacionCampos('Nombre',str,Utilities.notBlank,'no puede estar vacío.').title()

    telefono = f"+57 {Utilities.validacionCampos('Teléfono',str,Utilities.esDigito,'solo puede tener números.')}"
    
    email = Utilities.validacionEmail()
    
    mensaje = Funciones.crearCliente(idCliente,nombre,telefono,email)
    if mensaje:
        print(mensaje)
    else:
        print(f"El cliente {nombre} se creó correctamente.")


def inicioFacturacion():
    print("Para empezar un proceso de factuación, necesitamos los siguientes datos:")

    codigoMesa = Utilities.validacionCampos('Código de la mesa',int,Utilities.esDigito,"solo puede tener números.")

    idCliente = Utilities.validacionCampos('ID del cliente',int,Utilities.esDigito,"solo puede tener números.")

    factura = Funciones.facturar(codigoMesa,idCliente)
    
    if not isinstance(factura,dict):
        print(factura)
        return
    
    iniciarVenta(factura)


def iniciarVenta(factura):
    detalleFactura = []
    opcion = ""

    while(opcion != "0"):
        print("-"*35)
        print("""¿Qué quieres hacer a continuación?
    1. Agregar productos al pedido
    2. Sacar productos del pedido
    0. Finalizar pedido""")
        print("-"*35)
        opcion = input("Número de opción -> ")

        match(opcion):
            case "1":
                agregarProducto(detalleFactura)

            case "2":
                sacarProducto(detalleFactura)

            case "0":
                finalizarPedido(factura, detalleFactura)


def agregarProducto(detalleFactura):

    print("Para agregar un producto:")

    codigoProducto = Utilities.validacionCampos('Código del producto',int,Utilities.esDigito,'solo puede tener números.')

    cantidad = Utilities.validacionCampos('Cantidad a añadir',int,Utilities.campoNoNuloNiNegativo,'no puede ser nulo ni negativo.')

    mensaje = Funciones.agregarProducto(codigoProducto,cantidad,detalleFactura)

    if (mensaje):
        print(mensaje)
    else:
        print("El producto se agregó correctamente.")


def sacarProducto(detalleFactura):
    if len(detalleFactura) > 0:
        print("Para eliminar un producto del pedido:")
        
        codigoProducto = Utilities.validacionCampos('Código del producto',int,Utilities.esDigito,'solo puede tener números.')
        
        cantidad = Utilities.validacionCampos('Cantidad a eliminar',int,Utilities.campoNoNuloNiNegativo,'solo puede tener números.')

        encontrado = False
        for pedido in detalleFactura:
            if codigoProducto == pedido["ID_PRODUCTO"]:
                encontrado = True
                mensaje = Funciones.sacarProducto(codigoProducto,cantidad,detalleFactura)
                if mensaje:
                    print(mensaje)
                else:
                    print(f"Se quitaron {cantidad} unidades de {pedido['Nombre_Producto']} éxitosamente.")
                break

        if not encontrado:
            print("Ese producto no está en el pedido.")

    else:
        print("No se puede sacar productos del pedido porque está vacío.")


def finalizarPedido(factura, detalleFactura):
    print("Pedido finalizado: Generando factura...")
    Funciones.guardarInformacionFactura(factura,detalleFactura)
    
    facturaVisual = f"""
==========================================
            ACME RESTAURANT
==========================================
Fecha: {factura['Fecha']}
Mesa: {factura['Mesa']}
------------------------------------------
CLIENTE:
Nombre: {factura['Nombre_Cliente']}
ID: {factura['ID_CLIENTE']}
Tel: {factura['Teléfono']}
Email: {factura['Email']}
------------------------------------------
DETALLE:
Cod | Producto | Cant | V.Unit | IVA | Subtotal
"""
    totalFactura = 0
    for pedido in detalleFactura:
        linea = f"{pedido['ID_PRODUCTO']} | {pedido['Nombre_Producto']} | {pedido['Cantidad']}   | {pedido['Precio_unitario']}    | {pedido['IVA']}%   | {pedido['Subtotal']}\n"
        facturaVisual += linea
        totalFactura += float(pedido["Subtotal"])

    facturaVisual += "------------------------------------------"
    facturaVisual += f"\nTOTAL A PAGAR: ${round(totalFactura, 2)}"
    facturaVisual += "\n==========================================\n"

    print(facturaVisual)

    guardar = Utilities.guardarValidacion()
    if guardar:
        print("Guardando factura...")
        Funciones.guardarFacturaVisual(facturaVisual)
    else:
        print("Ha elegido no guardar la factura.")


def reporteVentas():
    while True:
        fecha = input("Ingrese la fecha para el reporte (DD/MM/AAAA) -> ").strip()
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            break
        except ValueError:
            print("Formato de fecha inválido. Use DD/MM/AAAA.")

    reporte = Funciones.generarReporte(fecha)

    if not reporte:
        print(f"No se encontraron ventas para la fecha {fecha}.")
        return

    reporteVisual = f"""
==========================================
        REPORTE DE VENTAS - ACME
==========================================
Fecha: {fecha}
------------------------------------------
Mesa | Total Productos | Subtotal Bruto | Subtotal IVA | Subtotal
"""

    totalVentaBruta = 0
    totalIVA = 0
    totalVentas = 0

    for fila in reporte:
        linea = f"{fila['Mesa']} | {fila['Total_Productos']} | ${fila['Subtotal_Bruto']} | ${fila['Subtotal_IVA']} | ${fila['Subtotal']}\n"
        reporteVisual += linea
        totalVentaBruta += fila["Subtotal_Bruto"]
        totalIVA += fila["Subtotal_IVA"]
        totalVentas += fila["Subtotal"]

    reporteVisual += "------------------------------------------"
    reporteVisual += f"\nTotal Venta Bruta: ${round(totalVentaBruta, 2)}"
    reporteVisual += f"\nTotal IVA: ${round(totalIVA, 2)}"
    reporteVisual += f"\nTotal Ventas: ${round(totalVentas, 2)}"
    reporteVisual += "\n==========================================\n"

    print(reporteVisual)

    guardar = Utilities.guardarValidacion()

    if guardar:
        Funciones.guardarReporteCSV(reporte, fecha, totalVentaBruta, totalIVA, totalVentas)
    else:
        print("Ha elegido no guardar el reporte.")
        

def facturar_con_descuento():
    print("\n--- PROCESO DE FACTURACIÓN CON DESCUENTO ---")
    
    id_mesa = Utilities.validacionCampos("Código de Mesa", int, Utilities.validacionPuestos, "debe ser entre 1 y 50")
    id_cliente = input("Identificación del Cliente -> ")
    
    # Aquí simulamos el subtotal.
    subtotal = 150000.0  
    
    print(f"Subtotal actual: ${subtotal}")
    aplica = input("¿Aplica descuento para esta factura? (Si/No): ").lower()
    
    porcentaje = 0
    if aplica in ["si", "sí"]:

        porcentaje = Utilities.validacionCampos("Porcentaje (0-50)", float, Funciones.validar_descuento, "debe estar entre 0 y 50")
    

    ahorro, total_final = Funciones.calcular_totales_factura(subtotal, porcentaje)
    
    
    print("\n" + "="*30)
    print(f"RESUMEN DE FACTURA - MESA {id_mesa}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Descuento ({porcentaje}%): -${ahorro:.2f}")
    print(f"TOTAL A PAGAR: ${total_final:.2f}")
    print("="*30)
    
    datos_factura = {
        "ID_MESA": id_mesa,
        "CLIENTE": id_cliente,
        "SUBTOTAL": subtotal,
        "PORCENTAJE_DESC": porcentaje,
        "VALOR_DESCUENTO": ahorro,
        "TOTAL": total_final,
        "FECHA": "16/04/2026" 
    }
    
    if Utilities.guardarValidacion():
        Funciones.exportar_factura_json(datos_factura,Funciones.rutaBase)
        print("Factura guardada y exportada a JSON.")
    
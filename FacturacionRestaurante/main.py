import App.Presentacion as App

opcion = ""
while(opcion != "0"):
    print("-"*35)
    print("ACME RESTAURANT")
    print("SISTEMA DE FACTURACIÓN")
    print("-"*35)
    print("""1. Crear producto
2. Crear mesa
3. Crear cliente
4. Facturación
5. Reporte de ventas
6. Descuentos especiales
0. Salir""")
    print("-"*35)

    opcion = input("Número de opción -> ")

    match(opcion):
        case "1":
            App.crearProducto()
        case "2":
            App.crearMesa()
        case "3":
            App.crearCliente()
        case "4":
            App.inicioFacturacion()
        case "5":
            App.reporteVentas()
        case "6":
            App.facturar_con_descuento()
        case "0":
            print("Hasta luego.")
        case _:
            print("Opción inválida. Intente de nuevo.")
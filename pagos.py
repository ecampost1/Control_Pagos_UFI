from db import obtener_conexion

def registrar_pago(id_estudiante, monto, metodo_pago):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        cursor.callproc("RegistrarPago", [id_estudiante, monto, metodo_pago])
        conexion.commit()

        cursor.close()
        conexion.close()
        print(f"Pago registrado para ID {id_estudiante}")


def generar_alertas():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.callproc("GenerarAlertasMorosidad")
        conexion.commit()
        cursor.close()
        conexion.close()
        print("⚠️ Alertas generadas correctamente")

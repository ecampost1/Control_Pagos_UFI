from db import obtener_conexion
import oracledb


# ==================== MATRÍCULAS ====================

def registrar_matricula(id_estudiante, anio, cuatrimestre, monto_total):
    """Registra una matrícula para un estudiante"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    REGISTRARMATRICULA(:1, :2, :3, :4);
                END;
            """, [id_estudiante, anio, cuatrimestre, monto_total])
            
            print(f" Matrícula registrada correctamente")
            return True
        except Exception as e:
            print(f" Error registrando matrícula: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()


def listar_matriculas_estudiante(id_estudiante):
    """Lista las matrículas de un estudiante específico"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARMATRICULASESTUDIANTE",
                oracledb.CURSOR,
                [id_estudiante]
            )
            
            matriculas = []
            for row in ref_cursor:
                matriculas.append({
                    'id_matricula': row[0],
                    'id_estudiante': row[1],
                    'anio': row[2],
                    'cuatrimestre': row[3],
                    'monto_total': row[4],
                    'nombre_completo': row[5]
                })
            
            ref_cursor.close()
            return matriculas
            
        except Exception as e:
            print(f" Error listando matrículas: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


def listar_todas_matriculas():
    """Lista todas las matrículas del sistema"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARTODASMATRICULAS",
                oracledb.CURSOR
            )
            
            matriculas = []
            for row in ref_cursor:
                matriculas.append({
                    'id_matricula': row[0],
                    'id_estudiante': row[1],
                    'nombre_completo': row[2],
                    'identificacion': row[3],
                    'anio': row[4],
                    'cuatrimestre': row[5],
                    'monto_total': row[6]
                })
            
            ref_cursor.close()
            return matriculas
            
        except Exception as e:
            print(f" Error listando matrículas: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


# ==================== PAGOS ====================

def registrar_pago(id_estudiante, monto, metodo_pago):
    """Registra un pago para un estudiante"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    REGISTRARPAGO(:1, :2, :3);
                END;
            """, [id_estudiante, monto, metodo_pago])
            
            print(f" Pago de ${monto} registrado correctamente")
            return True
        except Exception as e:
            print(f" Error registrando pago: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()


def listar_pagos_estudiante(id_estudiante):
    """Lista todos los pagos de un estudiante"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARPAGOSESTUDIANTE",
                oracledb.CURSOR,
                [id_estudiante]
            )
            
            pagos = []
            for row in ref_cursor:
                pagos.append({
                    'id_pago': row[0],
                    'id_estudiante': row[1],
                    'nombre_completo': row[2],
                    'fecha_pago': row[3],
                    'monto': row[4],
                    'metodo_pago': row[5],
                    'estado': row[6]
                })
            
            ref_cursor.close()
            return pagos
            
        except Exception as e:
            print(f" Error listando pagos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


def listar_todos_pagos():
    """Lista todos los pagos del sistema"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARTODOSPAGOS",
                oracledb.CURSOR
            )
            
            pagos = []
            for row in ref_cursor:
                pagos.append({
                    'id_pago': row[0],
                    'id_estudiante': row[1],
                    'nombre_completo': row[2],
                    'identificacion': row[3],
                    'fecha_pago': row[4],
                    'monto': row[5],
                    'metodo_pago': row[6],
                    'estado': row[7]
                })
            
            ref_cursor.close()
            return pagos
            
        except Exception as e:
            print(f" Error listando pagos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


# ==================== ESTADOS FINANCIEROS ====================

def obtener_estado_financiero(id_estudiante):
    """Obtiene el estado financiero de un estudiante"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "OBTENERESTADOFINANCIERO",
                oracledb.CURSOR,
                [id_estudiante]
            )
            
            estado = ref_cursor.fetchone()
            ref_cursor.close()
            
            if estado:
                return {
                    'id_estado': estado[0],
                    'id_estudiante': estado[1],
                    'nombre_completo': estado[2],
                    'identificacion': estado[3],
                    'saldo_actual': estado[4],
                    'ultima_actualizacion': estado[5],
                    'estado': estado[6]
                }
            return None
            
        except Exception as e:
            print(f" Error obteniendo estado financiero: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()


def listar_estados_financieros():
    """Lista todos los estados financieros"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARESTADOSFINANCIEROS",
                oracledb.CURSOR
            )
            
            estados = []
            for row in ref_cursor:
                estados.append({
                    'id_estado': row[0],
                    'id_estudiante': row[1],
                    'nombre_completo': row[2],
                    'identificacion': row[3],
                    'saldo_actual': row[4],
                    'ultima_actualizacion': row[5],
                    'estado': row[6]
                })
            
            ref_cursor.close()
            return estados
            
        except Exception as e:
            print(f" Error listando estados financieros: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


# ==================== ALERTAS DE MOROSIDAD ====================

def generar_alertas():
    """Genera alertas de morosidad para estudiantes con saldo pendiente"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    GENERARALERTASMOROSIDAD();
                END;
            """)
            
            print(" Alertas de morosidad generadas correctamente")
            return True
        except Exception as e:
            print(f" Error generando alertas: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()


def generar_alertas_prueba():
    """Genera alertas de prueba para TODOS los estudiantes con saldo pendiente"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    GENERARALERTASPRUEBA();
                END;
            """)
            
            print(" Alertas de prueba generadas")
            return True
        except Exception as e:
            print(f" Error generando alertas de prueba: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()


def listar_alertas_morosidad():
    """Lista todas las alertas de morosidad activas"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "LISTARALERTASMOROSIDAD",
                oracledb.CURSOR
            )
            
            alertas = []
            for row in ref_cursor:
                alertas.append({
                    'id_alerta': row[0],
                    'id_estudiante': row[1],
                    'nombre_completo': row[2],
                    'identificacion': row[3],
                    'correo': row[4],
                    'fecha_alerta': row[5],
                    'dias_mora': row[6],
                    'estado_alerta': row[7],
                    'saldo_actual': row[8]
                })
            
            ref_cursor.close()
            return alertas
            
        except Exception as e:
            print(f" Error listando alertas: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


def resolver_alerta(id_alerta):
    """Marca una alerta como resuelta"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    RESOLVERALERTA(:1);
                END;
            """, [id_alerta])
            
            print(f" Alerta {id_alerta} resuelta correctamente")
            return True
        except Exception as e:
            print(f" Error resolviendo alerta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

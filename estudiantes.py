from db import obtener_conexion
import oracledb


def insertar_estudiante(nombre, apellido, identificacion, correo):
    """Inserta un nuevo estudiante usando procedimiento almacenado"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    INSERTARESTUDIANTE(:1, :2, :3, :4);
                END;
            """, [nombre, apellido, identificacion, correo])
            
            conexion.commit()
            print(f" Estudiante '{nombre} {apellido}' insertado correctamente")
            return True
        except Exception as e:
            print(f"Error insertando estudiante: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()


def actualizar_estudiante(id_estudiante, nombre, apellido, identificacion, correo):
    """Actualiza los datos de un estudiante usando procedimiento almacenado"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    ACTUALIZARESTUDIANTE(:1, :2, :3, :4, :5);
                END;
            """, [id_estudiante, nombre, apellido, identificacion, correo])
            
            conexion.commit()
            print(f" Estudiante ID {id_estudiante} actualizado correctamente")
            return True
        except Exception as e:
            print(f" Error actualizando estudiante: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()


def actualizar_correo(id_estudiante, nuevo_correo):
    """Actualiza solo el correo de un estudiante (función legacy)"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    ACTUALIZARCORREOESTUDIANTE(:1, :2);
                END;
            """, [id_estudiante, nuevo_correo])
            
            conexion.commit()
            print(f" Correo actualizado para el estudiante {id_estudiante}")
            return True
        except Exception as e:
            print(f" Error: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()


def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante usando procedimiento almacenado"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                BEGIN
                    ELIMINARESTUDIANTE(:1);
                END;
            """, [id_estudiante])
            
            conexion.commit()
            print(f" Estudiante ID {id_estudiante} eliminado correctamente")
            return True
        except Exception as e:
            print(f" Error eliminando estudiante: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()


def obtener_estudiante(id_estudiante):
    """Obtiene un estudiante por ID usando función con cursor"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            
            ref_cursor = cursor.callfunc(
                "OBTENERESTUDIANTE",
                oracledb.CURSOR,
                [id_estudiante]
            )
            
            
            estudiante = ref_cursor.fetchone()
            ref_cursor.close()
            
            if estudiante:
                return {
                    'id': estudiante[0],
                    'nombre': estudiante[1],
                    'apellido': estudiante[2],
                    'identificacion': estudiante[3],
                    'correo': estudiante[4]
                }
            return None
            
        except Exception as e:
            print(f" Error obteniendo estudiante: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()


def listar_estudiantes():
    """Lista todos los estudiantes usando función con cursor"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            
            ref_cursor = cursor.callfunc(
                "LISTARESTUDIANTES",
                oracledb.CURSOR
            )
            
           
            estudiantes = []
            for row in ref_cursor:
                estudiantes.append({
                    'id': row[0],
                    'nombre': row[1],
                    'apellido': row[2],
                    'identificacion': row[3],
                    'correo': row[4]
                })
            
            ref_cursor.close()
            return estudiantes
            
        except Exception as e:
            print(f" Error listando estudiantes: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()


def buscar_estudiantes(termino):
    """Busca estudiantes por nombre, apellido o identificación usando función con cursor"""
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            ref_cursor = cursor.callfunc(
                "BUSCARESTUDIANTES",
                oracledb.CURSOR,
                [termino]
            )
            
           
            estudiantes = []
            for row in ref_cursor:
                estudiantes.append({
                    'id': row[0],
                    'nombre': row[1],
                    'apellido': row[2],
                    'identificacion': row[3],
                    'correo': row[4]
                })
            
            ref_cursor.close()
            return estudiantes
            
        except Exception as e:
            print(f" Error buscando estudiantes: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()



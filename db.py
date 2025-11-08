import oracledb
import config

def obtener_conexion():
    try:
        dsn = oracledb.makedsn(
            config.DB_HOST,
            config.DB_PORT,
            service_name=config.DB_SERVICE
        )

        conexion = oracledb.connect(
            user=config.DB_USER,
            password=config.DB_PASS,
            dsn=dsn
        )

        print("Conexión exitosa a Oracle")
        return conexion

    except oracledb.DatabaseError as e:
        print("Error de conexión:", e)
        return None

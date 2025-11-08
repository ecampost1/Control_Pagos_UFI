--------------------------------------------------------
--  File created - sábado-noviembre-08-2025   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure ACTUALIZARCORREOESTUDIANTE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."ACTUALIZARCORREOESTUDIANTE" (
    P_ID_ESTUDIANTE IN NUMBER,
    P_CORREO        IN VARCHAR2
) AS
BEGIN
    UPDATE Estudiantes
    SET Correo = P_CORREO
    WHERE ID_Estudiante = P_ID_ESTUDIANTE;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END ACTUALIZARCORREOESTUDIANTE;

/
--------------------------------------------------------
--  DDL for Procedure ACTUALIZARESTUDIANTE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."ACTUALIZARESTUDIANTE" (
    P_ID_ESTUDIANTE  IN NUMBER,
    P_NOMBRE         IN VARCHAR2,
    P_APELLIDO       IN VARCHAR2,
    P_IDENTIFICACION IN VARCHAR2,
    P_CORREO         IN VARCHAR2
) AS
BEGIN
    UPDATE Estudiantes
    SET Nombre = P_NOMBRE,
        Apellido = P_APELLIDO,
        Identificacion = P_IDENTIFICACION,
        Correo = P_CORREO
    WHERE ID_Estudiante = P_ID_ESTUDIANTE;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END ACTUALIZARESTUDIANTE;

/
--------------------------------------------------------
--  DDL for Procedure GENERARALERTASMOROSIDAD
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."GENERARALERTASMOROSIDAD" AS
CURSOR c_mora IS
SELECT ID_Estudiante, Saldo_Actual
FROM EstadosFinancieros
WHERE Saldo_Actual > 0;

v_id INT;
v_saldo DECIMAL(10,2);
BEGIN
  OPEN c_mora;
  LOOP
    FETCH c_mora INTO v_id, v_saldo;
    EXIT WHEN c_mora%NOTFOUND;

    INSERT INTO AlertasMorosidad (ID_Estudiante, Dias_Mora, Estado_Alerta)
    VALUES (v_id, 15, 'Pendiente');
  END LOOP;
  CLOSE c_mora;
END;

/
--------------------------------------------------------
--  DDL for Procedure ELIMINARESTUDIANTE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."ELIMINARESTUDIANTE" (
    P_ID_ESTUDIANTE IN NUMBER
) AS
BEGIN
    DELETE FROM Estudiantes
    WHERE ID_Estudiante = P_ID_ESTUDIANTE;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END ELIMINARESTUDIANTE;

/
--------------------------------------------------------
--  DDL for Procedure INSERTARESTUDIANTE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."INSERTARESTUDIANTE" (
    P_NOMBRE        IN VARCHAR2,
    P_APELLIDO      IN VARCHAR2,
    P_IDENTIFICACION IN VARCHAR2,
    P_CORREO        IN VARCHAR2
) AS
BEGIN
    INSERT INTO Estudiantes(Nombre, Apellido, Identificacion, Correo)
    VALUES (P_NOMBRE, P_APELLIDO, P_IDENTIFICACION, P_CORREO);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END INSERTARESTUDIANTE;

/

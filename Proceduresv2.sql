--------------------------------------------------------
--  File created - martes-diciembre-23-2025   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure RESOLVERALERTA
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."RESOLVERALERTA" (
    P_ID_ALERTA IN NUMBER
) AS
BEGIN
    UPDATE AlertasMorosidad
    SET Estado_Alerta = 'Resuelta'
    WHERE ID_Alerta = P_ID_ALERTA;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END RESOLVERALERTA;

/
--------------------------------------------------------
--  DDL for Procedure REGISTRARPAGO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."REGISTRARPAGO" (
    P_ID_ESTUDIANTE IN NUMBER,
    P_MONTO IN NUMBER,
    P_METODO_PAGO IN VARCHAR2
) AS
    v_total_matriculas NUMBER(10,2);
    v_total_pagos NUMBER(10,2);
    v_saldo NUMBER(10,2);
BEGIN
    -- Insertar el pago
    INSERT INTO Pagos (ID_Estudiante, Fecha_Pago, Monto, Metodo_Pago, Estado)
    VALUES (P_ID_ESTUDIANTE, SYSDATE, P_MONTO, P_METODO_PAGO, 'Procesado');
    
    -- Calcular total de matrículas
    SELECT NVL(SUM(Monto_Total), 0) 
    INTO v_total_matriculas
    FROM Matriculas 
    WHERE ID_Estudiante = P_ID_ESTUDIANTE;
    
    -- Calcular total de pagos
    SELECT NVL(SUM(Monto), 0) 
    INTO v_total_pagos
    FROM Pagos 
    WHERE ID_Estudiante = P_ID_ESTUDIANTE;
    
    -- Calcular el saldo
    v_saldo := v_total_matriculas - v_total_pagos;
    
    -- Actualizar o crear estado financiero
    MERGE INTO EstadosFinancieros EF
    USING (SELECT P_ID_ESTUDIANTE AS ID_EST FROM DUAL) D
    ON (EF.ID_Estudiante = D.ID_EST)
    WHEN MATCHED THEN
        UPDATE SET 
            Saldo_Actual = v_saldo,
            Ultima_Actualizacion = CURRENT_DATE
    WHEN NOT MATCHED THEN
        INSERT (ID_Estudiante, Saldo_Actual, Ultima_Actualizacion)
        VALUES (P_ID_ESTUDIANTE, v_saldo, CURRENT_DATE);
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END REGISTRARPAGO;

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
--  DDL for Procedure AGREGARLIBRO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."AGREGARLIBRO" (
    p_titulo IN VARCHAR2,
    p_autor IN VARCHAR2,
    p_copias_disponibles IN NUMBER
) AS
    v_mensaje VARCHAR2(200);
BEGIN
    -- Validar que las copias disponibles no sean negativas
    IF p_copias_disponibles < 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'El número de copias no puede ser negativo');
    END IF;

    -- Insertar el nuevo libro
    INSERT INTO Libros (titulo, autor, copias_disponibles)
    VALUES (p_titulo, p_autor, p_copias_disponibles);

    COMMIT;

    v_mensaje := 'Libro "' || p_titulo || '" agregado exitosamente con ' || 
                 p_copias_disponibles || ' copias disponibles.';
    DBMS_OUTPUT.PUT_LINE(v_mensaje);

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error al agregar el libro: ' || SQLERRM);
        RAISE;
END AgregarLibro;

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
--  DDL for Procedure GENERARALERTASMOROSIDAD
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."GENERARALERTASMOROSIDAD" AS
    CURSOR C_MOROSOS IS
        SELECT DISTINCT
            EF.ID_Estudiante,
            EF.Saldo_Actual,
            MIN(M.Fecha_Vencimiento) AS Fecha_Vencimiento_Mas_Antigua,
            GREATEST(
                TRUNC(SYSDATE - MIN(M.Fecha_Vencimiento)),
                0
            ) AS Dias_Vencidos
        FROM EstadosFinancieros EF
        INNER JOIN Matriculas M ON EF.ID_Estudiante = M.ID_Estudiante
        WHERE EF.Saldo_Actual > 0
          AND M.Fecha_Vencimiento < SYSDATE  -- Matrícula vencida
        GROUP BY EF.ID_Estudiante, EF.Saldo_Actual
        HAVING GREATEST(TRUNC(SYSDATE - MIN(M.Fecha_Vencimiento)), 0) > 0;
    
    V_EXISTE NUMBER;
    V_CONTADOR NUMBER := 0;
BEGIN
    FOR R IN C_MOROSOS LOOP
        -- Verificar si ya existe alerta pendiente para este estudiante
        SELECT COUNT(*) INTO V_EXISTE
        FROM AlertasMorosidad
        WHERE ID_Estudiante = R.ID_Estudiante
          AND Estado_Alerta = 'Pendiente';
        
        -- Si no existe, crear alerta nueva
        IF V_EXISTE = 0 THEN
            INSERT INTO AlertasMorosidad (
                ID_Estudiante, 
                Fecha_Alerta, 
                Dias_Mora, 
                Estado_Alerta
            )
            VALUES (
                R.ID_Estudiante,
                SYSDATE,
                R.Dias_Vencidos,
                'Pendiente'
            );
            V_CONTADOR := V_CONTADOR + 1;
        ELSE
            -- Si ya existe, actualizar los días de mora
            UPDATE AlertasMorosidad
            SET Dias_Mora = R.Dias_Vencidos,
                Fecha_Alerta = SYSDATE
            WHERE ID_Estudiante = R.ID_Estudiante
              AND Estado_Alerta = 'Pendiente';
            V_CONTADOR := V_CONTADOR + 1;
        END IF;
    END LOOP;
    
    COMMIT;
    
    -- Informar cuántas alertas se procesaron
    DBMS_OUTPUT.PUT_LINE('Alertas procesadas: ' || V_CONTADOR);
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END GENERARALERTASMOROSIDAD;

/
--------------------------------------------------------
--  DDL for Procedure REGISTRARMATRICULA
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."REGISTRARMATRICULA" (
    P_ID_ESTUDIANTE IN NUMBER,
    P_ANIO IN NUMBER,
    P_CUATRIMESTRE IN NUMBER,
    P_MONTO_TOTAL IN NUMBER,
    P_DIAS_VENCIMIENTO IN NUMBER DEFAULT 30
) AS
    V_FECHA_VENCIMIENTO DATE;
BEGIN
    -- Calcular fecha de vencimiento
    V_FECHA_VENCIMIENTO := SYSDATE + P_DIAS_VENCIMIENTO;
    
    -- Insertar matrícula con fecha de vencimiento
    INSERT INTO Matriculas (ID_Estudiante, Año, Cuatrimestre, Monto_Total, Fecha_Vencimiento)
    VALUES (P_ID_ESTUDIANTE, P_ANIO, P_CUATRIMESTRE, P_MONTO_TOTAL, V_FECHA_VENCIMIENTO);
    
    -- Crear o actualizar estado financiero
    MERGE INTO EstadosFinancieros EF
    USING (SELECT P_ID_ESTUDIANTE AS ID_EST FROM DUAL) D
    ON (EF.ID_Estudiante = D.ID_EST)
    WHEN MATCHED THEN
        UPDATE SET 
            Saldo_Actual = Saldo_Actual + P_MONTO_TOTAL,
            Ultima_Actualizacion = CURRENT_DATE
    WHEN NOT MATCHED THEN
        INSERT (ID_Estudiante, Saldo_Actual, Ultima_Actualizacion)
        VALUES (P_ID_ESTUDIANTE, P_MONTO_TOTAL, CURRENT_DATE);
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END REGISTRARMATRICULA;

/
--------------------------------------------------------
--  DDL for Procedure GENERARALERTASPRUEBA
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."GENERARALERTASPRUEBA" AS
    CURSOR C_DEUDORES IS
        SELECT 
            EF.ID_Estudiante,
            EF.Saldo_Actual,
            TRUNC(SYSDATE - EF.Ultima_Actualizacion) AS Dias_Sin_Pago
        FROM EstadosFinancieros EF
        WHERE EF.Saldo_Actual > 0;
    
    V_EXISTE NUMBER;
    V_CONTADOR NUMBER := 0;
BEGIN
    FOR R IN C_DEUDORES LOOP
        -- Verificar si ya existe alerta pendiente
        SELECT COUNT(*) INTO V_EXISTE
        FROM AlertasMorosidad
        WHERE ID_Estudiante = R.ID_Estudiante
          AND Estado_Alerta = 'Pendiente';
        
        -- Si no existe, crear alerta
        IF V_EXISTE = 0 THEN
            INSERT INTO AlertasMorosidad (
                ID_Estudiante, 
                Fecha_Alerta, 
                Dias_Mora, 
                Estado_Alerta
            )
            VALUES (
                R.ID_Estudiante,
                SYSDATE,
                GREATEST(R.Dias_Sin_Pago, 1),  -- Mínimo 1 día
                'Pendiente'
            );
            V_CONTADOR := V_CONTADOR + 1;
        END IF;
    END LOOP;
    
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Alertas de prueba creadas: ' || V_CONTADOR);
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END GENERARALERTASPRUEBA;

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

--------------------------------------------------------
--  File created - martes-diciembre-23-2025   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function BUSCARESTUDIANTES
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."BUSCARESTUDIANTES" (
    P_TERMINO IN VARCHAR2
) RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT ID_Estudiante, Nombre, Apellido, Identificacion, Correo
        FROM Estudiantes
        WHERE UPPER(Nombre) LIKE '%' || UPPER(P_TERMINO) || '%'
           OR UPPER(Apellido) LIKE '%' || UPPER(P_TERMINO) || '%'
           OR UPPER(Identificacion) LIKE '%' || UPPER(P_TERMINO) || '%'
        ORDER BY ID_Estudiante;

    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END BUSCARESTUDIANTES;

/
--------------------------------------------------------
--  DDL for Function CALCULARSALDO
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."CALCULARSALDO" (
    p_id_estudiante IN INT
) RETURN DECIMAL AS
    v_total_matriculas DECIMAL(10,2);
    v_total_pagos DECIMAL(10,2);
BEGIN
    SELECT NVL(SUM(Monto_Total),0) INTO v_total_matriculas
    FROM Matriculas WHERE ID_Estudiante = p_id_estudiante;

    SELECT NVL(SUM(Monto),0) INTO v_total_pagos
    FROM Pagos WHERE ID_Estudiante = p_id_estudiante;

    RETURN (v_total_matriculas - v_total_pagos);
END;

/
--------------------------------------------------------
--  DDL for Function LISTARALERTASMOROSIDAD
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARALERTASMOROSIDAD" 
RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            A.ID_Alerta,
            A.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            E.Identificacion,
            E.Correo,
            A.Fecha_Alerta,
            A.Dias_Mora,
            A.Estado_Alerta,
            NVL(EF.Saldo_Actual, 0) AS Saldo_Actual
        FROM AlertasMorosidad A
        INNER JOIN Estudiantes E ON A.ID_Estudiante = E.ID_Estudiante
        LEFT JOIN EstadosFinancieros EF ON A.ID_Estudiante = EF.ID_Estudiante
        WHERE A.Estado_Alerta = 'Pendiente'
        ORDER BY A.Dias_Mora DESC, A.Fecha_Alerta DESC;
    
    RETURN V_CURSOR;
END LISTARALERTASMOROSIDAD;

/
--------------------------------------------------------
--  DDL for Function LISTARESTADOSFINANCIEROS
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARESTADOSFINANCIEROS" 
RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            EF.ID_Estado,
            EF.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            E.Identificacion,
            EF.Saldo_Actual,
            EF.Ultima_Actualizacion,
            CASE 
                WHEN EF.Saldo_Actual > 0 THEN 'Debe'
                WHEN EF.Saldo_Actual < 0 THEN 'A Favor'
                ELSE 'Al Día'
            END AS Estado
        FROM EstadosFinancieros EF
        INNER JOIN Estudiantes E ON EF.ID_Estudiante = E.ID_Estudiante
        ORDER BY EF.Saldo_Actual DESC;
    
    RETURN V_CURSOR;
END LISTARESTADOSFINANCIEROS;

/
--------------------------------------------------------
--  DDL for Function LISTARESTUDIANTES
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARESTUDIANTES" 
RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT ID_Estudiante, Nombre, Apellido, Identificacion, Correo
        FROM Estudiantes
        ORDER BY ID_Estudiante;

    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END LISTARESTUDIANTES;

/
--------------------------------------------------------
--  DDL for Function LISTARMATRICULASESTUDIANTE
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARMATRICULASESTUDIANTE" (
    P_ID_ESTUDIANTE IN NUMBER
) RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            M.ID_Matricula,
            M.ID_Estudiante,
            M.Año,
            M.Cuatrimestre,
            M.Monto_Total,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto
        FROM Matriculas M
        INNER JOIN Estudiantes E ON M.ID_Estudiante = E.ID_Estudiante
        WHERE M.ID_Estudiante = P_ID_ESTUDIANTE
        ORDER BY M.Año DESC, M.Cuatrimestre DESC;
    
    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END LISTARMATRICULASESTUDIANTE;

/
--------------------------------------------------------
--  DDL for Function LISTARPAGOSESTUDIANTE
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARPAGOSESTUDIANTE" (
    P_ID_ESTUDIANTE IN NUMBER
) RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            P.ID_Pago,
            P.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            P.Fecha_Pago,
            P.Monto,
            P.Metodo_Pago,
            P.Estado
        FROM Pagos P
        INNER JOIN Estudiantes E ON P.ID_Estudiante = E.ID_Estudiante
        WHERE P.ID_Estudiante = P_ID_ESTUDIANTE
        ORDER BY P.Fecha_Pago DESC;
    
    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END LISTARPAGOSESTUDIANTE;

/
--------------------------------------------------------
--  DDL for Function LISTARTODASMATRICULAS
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARTODASMATRICULAS" 
RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            M.ID_Matricula,
            M.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            E.Identificacion,
            M.Año,
            M.Cuatrimestre,
            M.Monto_Total
        FROM Matriculas M
        INNER JOIN Estudiantes E ON M.ID_Estudiante = E.ID_Estudiante
        ORDER BY M.Año DESC, M.Cuatrimestre DESC, E.Apellido;
    
    RETURN V_CURSOR;
END LISTARTODASMATRICULAS;

/
--------------------------------------------------------
--  DDL for Function LISTARTODOSPAGOS
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."LISTARTODOSPAGOS" 
RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            P.ID_Pago,
            P.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            E.Identificacion,
            P.Fecha_Pago,
            P.Monto,
            P.Metodo_Pago,
            P.Estado
        FROM Pagos P
        INNER JOIN Estudiantes E ON P.ID_Estudiante = E.ID_Estudiante
        ORDER BY P.Fecha_Pago DESC;
    
    RETURN V_CURSOR;
END LISTARTODOSPAGOS;

/
--------------------------------------------------------
--  DDL for Function OBTENERESTADOFINANCIERO
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."OBTENERESTADOFINANCIERO" (
    P_ID_ESTUDIANTE IN NUMBER
) RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT 
            EF.ID_Estado,
            EF.ID_Estudiante,
            E.Nombre || ' ' || E.Apellido AS NombreCompleto,
            E.Identificacion,
            EF.Saldo_Actual,
            EF.Ultima_Actualizacion,
            CASE 
                WHEN EF.Saldo_Actual > 0 THEN 'Debe'
                WHEN EF.Saldo_Actual < 0 THEN 'A Favor'
                ELSE 'Al Día'
            END AS Estado
        FROM EstadosFinancieros EF
        INNER JOIN Estudiantes E ON EF.ID_Estudiante = E.ID_Estudiante
        WHERE EF.ID_Estudiante = P_ID_ESTUDIANTE;
    
    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END OBTENERESTADOFINANCIERO;

/
--------------------------------------------------------
--  DDL for Function OBTENERESTUDIANTE
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."OBTENERESTUDIANTE" (
    P_ID_ESTUDIANTE IN NUMBER
) RETURN SYS_REFCURSOR AS
    V_CURSOR SYS_REFCURSOR;
BEGIN
    OPEN V_CURSOR FOR
        SELECT ID_Estudiante, Nombre, Apellido, Identificacion, Correo
        FROM Estudiantes
        WHERE ID_Estudiante = P_ID_ESTUDIANTE;

    RETURN V_CURSOR;
EXCEPTION
    WHEN OTHERS THEN
        IF V_CURSOR%ISOPEN THEN
            CLOSE V_CURSOR;
        END IF;
        RAISE;
END OBTENERESTUDIANTE;

/

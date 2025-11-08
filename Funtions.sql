--------------------------------------------------------
--  File created - sábado-noviembre-08-2025   
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

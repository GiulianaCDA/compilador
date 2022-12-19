DIM n AS INT

FUNCTION par(k AS INT) AS INT
    IF k == 1 THEN
        LET n = 0
    END IF
    IF k == 0 THEN
        LET n = 1
    END IF
    CALL par(k - 2)
END FUNCTION

CALL par(4)
END
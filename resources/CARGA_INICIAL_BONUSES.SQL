-- SCRIPT CARGA INICIAL BONUSES
DECLARE 
    CURSOR CUR_BONUSES IS 
        SELECT * 
        FROM CHARGES CH
        WHERE UNIT_PRICE < 0
        AND CHARGE_DT BETWEEN TO_DATE('01-01-1999','DD-MM-YYYY') AND TO_DATE('01-01-2000','DD-MM-YYYY')
        AND NOT EXISTS (
            SELECT 1 
            FROM MAIN_BONUSES MB
            WHERE CH.CHARGE_ID = MB.BONUS_ID);

    v_event         VARCHAR2(100); 
    v_type          VARCHAR2(100); 
    v_status        VARCHAR2(100);
    v_charge_type   VARCHAR2(100);
    v_marketplace   VARCHAR2(100);
    v_amount        NUMBER(12,2);
    v_app_id        VARCHAR2(100);
    v_charge_id     NUMBER(20); 
    v_code          NUMBER;
    v_errm          VARCHAR2(512);
    v_sysdate       DATE;

BEGIN
    v_event := 'INIT_LOAD';
    v_sysdate := SYSDATE; 

    FOR REG IN CUR_BONUSES LOOP
        
        BEGIN
            v_charge_id := REG.CHARGE_ID;
            v_amount := abs(REG.UNIT_PRICE * REG.QUANTITY);
            v_charge_type := REG.CHARGE_TYPE_ID;         
            SELECT marketplace_id into v_marketplace FROM CHARGE_TYPE WHERE type_id = v_charge_type;  

            IF REG.CHARGE_STATUS = 'I' THEN
                v_status := 'I';
            ELSE
                v_status := 'A';    
            END IF;   

            IF REG.FROM_USER is not NULL THEN
                v_app_id := REG.FROM_USER;
            ELSE
                v_app_id := REG.FROM_PRG;
            END IF; 

            INSERT INTO MAIN_BONUSES ( 
                BONUS_ID, CHARGE_ID, CUST_ID, SITE_ID, AMOUNT, CURRENCY_ID, TYPE, STATUS, MARKETPLACE, DATE_CREATED, LAST_UPDATED, BONUS_DATE, APP_ID ) 
            VALUES ( 
                REG.CHARGE_ID, REG.REF_CHARGE_ID, REG.CUST_ID, REG.SITE_ID, v_amount, REG.CURRENCY_ID, v_charge_type, v_status, v_marketplace, REG.INS_DT, v_sysdate, REG.CHARGE_DT, v_app_id );

            COMMIT; 

        EXCEPTION
            WHEN OTHERS THEN
                v_code := SQLCODE;
                v_errm := SUBSTR(SQLERRM, 1, 512);
                
                INSERT INTO CHARGES_ERRORS (
                    ID, DATE_CREATED, EVENT, CHARGE_ID, ERROR_MESSAGE)
                VALUES (
                    SEQ_CHARGES_ERRORS_ID.NEXTVAL, v_sysdate, v_event, v_charge_id, 'Error_Code: ' || v_code || ', Error_Message: ' || v_errm );

                COMMIT;
        END;

    END LOOP; 

    COMMIT; 
    
EXCEPTION 
    WHEN OTHERS THEN 
        v_code := SQLCODE;
        v_errm := SUBSTR(SQLERRM, 1, 512);

        INSERT INTO CHARGES_ERRORS (
            ID, DATE_CREATED, EVENT, CHARGE_ID, ERROR_MESSAGE)
        VALUES (
            SEQ_CHARGES_ERRORS_ID.NEXTVAL, v_sysdate, v_event, v_charge_id, 'Error_Code: ' || v_code || ', Error_Message: ' || v_errm );

        COMMIT; 
END;
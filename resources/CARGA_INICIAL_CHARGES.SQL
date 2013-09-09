-- SCRIPT CARGA INICIAL CHARGES
DECLARE 
    CURSOR CUR_CHARGES IS 
        SELECT * 
        FROM CHARGES CH
        WHERE UNIT_PRICE >= 0
        --AND CHARGE_DT >= TO_DATE('01-01-2011','DD-MM-YYYY')
        AND NOT EXISTS (
            SELECT 1 
            FROM MAIN_CHARGES MCH
            WHERE CH.CHARGE_ID = MCH.CHARGE_ID);

    v_event         VARCHAR2(100); 
    v_type          VARCHAR2(100); 
    v_status        VARCHAR2(100);
    v_charge_type   VARCHAR2(100);
    v_marketplace   VARCHAR2(100);
    v_amount        NUMBER(12,2);
    v_from_id       VARCHAR2(100);
    v_charge_id     NUMBER(20); 
    v_code          NUMBER;
    v_errm          VARCHAR2(512);
    v_sysdate       DATE;

BEGIN
    v_event := 'INIT_LOAD';
    v_sysdate := SYSDATE; 
    
    FOR REG IN CUR_CHARGES LOOP
        
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
                v_from_id := REG.FROM_USER;
            ELSE
                v_from_id := REG.FROM_PRG;
            END IF; 

            --INSERTO EN LA MAIN_CHARGES
            INSERT INTO MAIN_CHARGES ( 
                CHARGE_ID, CUST_ID, SITE_ID, AMOUNT, CURRENCY_ID, TYPE, STATUS, MARKETPLACE, DATE_CREATED, LAST_MODIFIED, CHARGE_DATE_CREATED, FROM_ID ) 
            VALUES ( 
                REG.CHARGE_ID, REG.CUST_ID, REG.SITE_ID, v_amount, REG.CURRENCY_ID, v_charge_type, v_status, v_marketplace, REG.INS_DT, v_sysdate, REG.CHARGE_DT, v_from_id );

            --INSERTO EN LAS SATÉLITES
            --SYI_ORDER
            IF REG.ITEM_ID is not NULL OR REG.UNIT_PRICE is not NULL OR REG.QUANTITY is not NULL THEN
                INSERT INTO SYI_ORDER (
                    CHARGE_ID, ITEM_ID, UNIT_PRICE, QUANTITY )
                VALUES ( 
                    REG.CHARGE_ID, REG.ITEM_ID, REG.UNIT_PRICE, REG.QUANTITY );
            END IF; 

            --PMS
            IF REG.AFF_CHARGE_PRICE is not NULL OR REG.AFF_SITE_CHARGE is not NULL OR REG.AFF_PYMNT_CHARGE is not NULL THEN
                INSERT INTO PMS (
                    CHARGE_ID, AFF_CHARGE_PRICE, AFF_SITE_CHARGE, AFF_PYMNT_CHARGE )
                VALUES (
                    REG.CHARGE_ID, REG.AFF_CHARGE_PRICE, REG.AFF_SITE_CHARGE, REG.AFF_PYMNT_CHARGE );
            END IF; 

            --OTHER_DATA 
            IF REG.ORIG_CURRENCY is not NULL OR REG.ORIG_ITEM_CURRENCY is not NULL OR REG.ORIG_UNIT_PRICE is not NULL OR REG.ORIG_ITEM_UNIT_PRICE is not NULL OR REG.COLLECTED_AMOUNT is not NULL THEN
                INSERT INTO OTHER_MAIN_CHARGES_DATA (
                    CHARGE_ID, ORIG_CURRENCY, ORIG_ITEM_CURRENCY, ORIG_UNIT_PRICE, ORIG_ITEM_UNIT_PRICE, COLLECTED_AMOUNT )
                VALUES ( 
                    REG.CHARGE_ID, REG.ORIG_CURRENCY, REG.ORIG_ITEM_CURRENCY, REG.ORIG_UNIT_PRICE, REG.ORIG_ITEM_UNIT_PRICE, REG.COLLECTED_AMOUNT );        
            END IF; 

            COMMIT; 

        EXCEPTION 
            WHEN OTHERS THEN
                ROLLBACK; 

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

        ROLLBACK;

        INSERT INTO CHARGES_ERRORS (
            ID, DATE_CREATED, EVENT, CHARGE_ID, ERROR_MESSAGE )
        VALUES (
            SEQ_CHARGES_ERRORS_ID.NEXTVAL, v_sysdate, v_event, v_charge_id, 'Error_Code: ' || v_code || ', Error_Message: ' || v_errm );

        COMMIT;
END;
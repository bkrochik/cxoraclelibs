import unittest
import sys
sys.path.append('libs')
import dbConnection

class TestSequenceFunctions(unittest.TestCase):
    
    @staticmethod
    def createDict(cursor):
        fieldNumber = 0
        fieldNames={}
        for desc in cursor.description:
            fieldNames[desc[0]]=fieldNumber
            fieldNumber+=1
        return [cursor.fetchall(),fieldNames]

    def setUp(self):
        #Insert test data
        cur.execute("INSERT INTO CHARGES (CURRENCY_ID,SITE_ID,CHARGE_TYPE_ID,DOC_ID,CHARGE_ID,CUST_ID,CATEG_ID,ITEM_ID,QUANTITY,UNIT_PRICE,CHARGE_DT,CHARGE_STATUS,PAY_STATUS,INS_DT,REF_CHARGE_ID,BID_CUST_ID,PAY_AMOUNT,BID_SEQUENCE,CUST_SITE,ORIG_CURRENCY,DOL_UNIT_PRICE,ORIG_UNIT_PRICE,ORIG_ITEM_UNIT_PRICE,FROM_PRG,ORIG_ITEM_CURRENCY,FROM_USER,COMMENTS,BONIF_STATUS,COLLECTED_AMOUNT,MAIL_BONIF,PREPAY,AFF_SITE_CHARGE,AFF_PYMNT_CHARGE,TIMESTAMP,QTY_BONIF,AFF_CHARGE_PRICE,SEARCH_WORD,COMBO_TYPE_ID) VALUES ('MEX','MLM','CV',358008,4112095,10003446,'1832',3534564,1,0.97,TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),'F','T',TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),NULL,NULL,0.97,1,'MLM','DOL',0.1,0.1,0.1,NULL,'DOL',NULL,NULL,NULL,NULL,NULL,NULL,219639,11552,TO_DATE('03-JUL-2006 11:23:26','DD-MON-RRRR HH24:MI:SS'),0,0.97,NULL,NULL)")

        #Obtengo el id del insertado
        cur.execute('select * from CHARGES where rownum<=1 order by TIMESTAMP desc')

        #Armo diccionario de datos
        dict=self.createDict(cur);
        result=dict[0]
        fieldNames=dict[1]

        for row in result:
            self.chargeId=row[fieldNames['CHARGE_ID']]
            self.custId=row[fieldNames['CUST_ID']]
            self.siteId=row[fieldNames['SITE_ID']]
            self.unitPrice=row[fieldNames['UNIT_PRICE']]
            self.quantity=row[fieldNames['QUANTITY']]
            self.currencyId=row[fieldNames['CURRENCY_ID']]
            self.itemId=row[fieldNames['ITEM_ID']]
            self.type=row[fieldNames['CHARGE_TYPE_ID']]
            self.status=row[fieldNames['CHARGE_STATUS']]
            self.marketplace=row[fieldNames['CHARGE_TYPE_ID']]
            self.dateCreated=row[fieldNames['INS_DT']]
            self.chargeDateCreated=row[fieldNames['CHARGE_DT']]
            self.fromId=row[fieldNames['FROM_PRG']]
            self.affChargePrice=row[fieldNames['AFF_CHARGE_PRICE']]
            self.affSiteCharge=row[fieldNames['AFF_SITE_CHARGE']]
            self.affPymntCharge=row[fieldNames['AFF_PYMNT_CHARGE']]
            self.origCurrency=row[fieldNames['ORIG_CURRENCY']]
            self.oringUnitPrice=row[fieldNames['ORIG_UNIT_PRICE']]
            self.origItemCurrency=row[fieldNames['ORIG_ITEM_CURRENCY']]
            self.origItemUnitPrice=row[fieldNames['ORIG_ITEM_UNIT_PRICE']]
            self.collectedAmount=row[fieldNames['COLLECTED_AMOUNT']]

    def test1_insert_on_main_charges(self): 
        #Consultas
        cur.execute('select * from MAIN_CHARGES where CHARGE_ID=%s and rownum<=1' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(cur);
        result=dict[0]
        fieldNames=dict[1]

        #Cantidad de registros insertados
        self.assertEqual(len(result),1)

        for row in result:
            self.assertEqual(row[fieldNames['CHARGE_ID']],self.chargeId)
            self.assertEqual(row[fieldNames['CUST_ID']],self.custId)
            self.assertEqual(row[fieldNames['SITE_ID']],self.siteId)
            self.assertEqual(row[fieldNames['AMOUNT']],self.unitPrice*self.quantity)
            self.assertEqual(row[fieldNames['TYPE']],self.type)
            self.assertEqual(row[fieldNames['CHARGE_DATE_CREATED']],self.chargeDateCreated)
            self.assertEqual(row[fieldNames['FROM_ID']],self.fromId)

            #Status transformation
            if self.status=='I':
                self.assertEqual(row[fieldNames['STATUS']],'I')
            else:
                self.assertEqual(row[fieldNames['STATUS']],'A')

    def test2_insert_on_syi_order(self):
        #Consultas
        cur.execute('select * from SYI_ORDER where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
        
        if self.itemId != None or self.quantity != None or self.unitPrice != None:
        
            #Armo diccionario de datos
            dict=self.createDict(cur);
            result=dict[0]
            fieldNames=dict[1]
            
            #Cantidad de registros insertados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['CHARGE_ID']],self.chargeId)
                self.assertEqual(row[fieldNames['ITEM_ID']],self.itemId)
                self.assertEqual(row[fieldNames['QUANTITY']],self.quantity)
                self.assertEqual(row[fieldNames['UNIT_PRICE']],self.unitPrice)
        else:
            #Cantidad de registros insertados
            self.assertEqual(len(resultset),0)

    def test3_insert_on_pms(self):
        #Consultas
        cur.execute('select * from PMS where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
     
        if self.affPymntCharge != None or self.affSiteCharge != None or self.affChargePrice != None:

            #Armo diccionario de datos
            dict=self.createDict(cur);
            result=dict[0]
            fieldNames=dict[1]
            
            #Cantidad de registros insertados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['CHARGE_ID']],self.chargeId)
                self.assertEqual(row[fieldNames['AFF_PYMNT_CHARGE']],self.affPymntCharge)
                self.assertEqual(row[fieldNames['AFF_SITE_CHARGE']],self.affSiteCharge)
                self.assertEqual(row[fieldNames['AFF_CHARGE_PRICE']],self.affChargePrice)

        else:
            #Cantidad de registros insertados
            self.assertEqual(len(resultset),0)

    def test4_insert_on_other_main_charges_data(self):
        #Consultas
        cur.execute('select * from OTHER_MAIN_CHARGES_DATA where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
     
        if self.origCurrency != None or self.oringUnitPrice != None or self.origItemCurrency != None or self.origItemUnitPrice != None or self.collectedAmount != None:

            #Armo diccionario de datos
            dict=self.createDict(cur);
            result=dict[0]
            fieldNames=dict[1]

            #Cantidad de registros insertados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['CHARGE_ID']],self.chargeId)
                self.assertEqual(row[fieldNames['ORIG_CURRENCY']],self.origCurrency)
                self.assertEqual(row[fieldNames['ORIG_UNIT_PRICE']],self.oringUnitPrice)
                self.assertEqual(row[fieldNames['ORIG_ITEM_CURRENCY']],self.origItemCurrency)
                self.assertEqual(row[fieldNames['ORIG_ITEM_UNIT_PRICE']],self.origItemUnitPrice)
                self.assertEqual(row[fieldNames['COLLECTED_AMOUNT']],self.collectedAmount)

        else:
            #Cantidad de registros insertados
            self.assertEqual(len(resultset),0)

    def test5_insert_on_feed_charges(self):
        #Consultas
        cur.execute('select * from FEED_CHARGES where CHARGE_ID=%s and rownum<=1' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(cur);
        result=dict[0]
        fieldNames=dict[1]
            
        #Cantidad de registros insertados
        self.assertEqual(len(result),1)

         #Valores insertados
        for row in result:
            self.assertEqual(row[fieldNames['CHARGE_ID']],self.chargeId)
            self.assertEqual(row[fieldNames['TYPE']],'C')
            self.assertEqual(row[fieldNames['CHARGE_DATE']],self.chargeDateCreated)
    
    def test6_delete_loaded_data(self):
        #Delete test 
        try:
            cur.execute('delete from CHARGES where CHARGE_ID = %s' % (self.chargeId))
            cur.execute('delete from MAIN_CHARGES where CHARGE_ID = %s' % (self.chargeId))
            cur.execute('delete from FEED_CHARGES where CHARGE_ID = %s' % (self.chargeId))
            cur.execute('delete from PMS where CHARGE_ID = %s' % (self.chargeId))
            cur.execute('delete from SYI_ORDER where CHARGE_ID = %s' % (self.chargeId))
            cur.execute('delete from OTHER_MAIN_CHARGES_DATA where CHARGE_ID = %s' % (self.chargeId))
            self.assertTrue(1,1)  
        except ValueError:
            self.assertTrue(1,2)

if __name__ == '__main__':
    #Init DB
    db=dbConnection.getDBCursor('10.0.10.26',1521,'desa11g','billing','GHaURU13')
    cur=db.cursor()
    #Init test fw
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #Close connection
    db.commit()
    cur.close() 
    db.close()

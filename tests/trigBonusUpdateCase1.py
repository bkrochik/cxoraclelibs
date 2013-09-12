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
        #Init DB
        self.db=dbConnection.getDBCursor('10.0.10.26',1521,'desa11g','billing','GHaURU13')
        self.cur=self.db.cursor()

        #Insert test data
        self.cur.execute("INSERT INTO CHARGES (CURRENCY_ID,SITE_ID,CHARGE_TYPE_ID,DOC_ID,CHARGE_ID,CUST_ID,CATEG_ID,ITEM_ID,QUANTITY,UNIT_PRICE,CHARGE_DT,CHARGE_STATUS,PAY_STATUS,INS_DT,REF_CHARGE_ID,BID_CUST_ID,PAY_AMOUNT,BID_SEQUENCE,CUST_SITE,ORIG_CURRENCY,DOL_UNIT_PRICE,ORIG_UNIT_PRICE,ORIG_ITEM_UNIT_PRICE,FROM_PRG,ORIG_ITEM_CURRENCY,FROM_USER,COMMENTS,BONIF_STATUS,COLLECTED_AMOUNT,MAIL_BONIF,PREPAY,AFF_SITE_CHARGE,AFF_PYMNT_CHARGE,TIMESTAMP,QTY_BONIF,AFF_CHARGE_PRICE,SEARCH_WORD,COMBO_TYPE_ID) VALUES ('$','IBZ','BV',347692,4284859,10837411,NULL,6759204,1,-0.97,TO_DATE('13-AUG-2002 22:47:39','DD-MON-RRRR HH24:MI:SS'),'F','I',TO_DATE('04-SEP-2002 13:13:21','DD-MON-RRRR HH24:MI:SS'),4112436,10205213,NULL,1,'MLB','REA',-1.92,-6,NULL,'MED',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,TO_DATE('23-MAY-2008 12:14:27','DD-MON-RRRR HH24:MI:SS'),NULL,NULL,NULL,NULL)");
        self.db.commit()
        #Update
        self.cur.execute("UPDATE CHARGES SET CURRENCY_ID='u$s',SITE_ID='MLA',ITEM_ID=321,AFF_PYMNT_CHARGE=321,AFF_CHARGE_PRICE=321,AFF_SITE_CHARGE=321,ORIG_CURRENCY='TST',ORIG_UNIT_PRICE=321,ORIG_ITEM_CURRENCY='%',ORIG_ITEM_UNIT_PRICE=321,CHARGE_TYPE_ID='BV' WHERE CHARGE_ID=4284859")
        self.db.commit()
        #Obtengo el id del cargo actualizado
        self.cur.execute('select * from CHARGES where rownum<=1 and CHARGE_ID=4284859 order by TIMESTAMP desc')
       
        #Armo diccionario de datos
        dict=self.createDict(self.cur);
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

    def test1_update_on_main_bonuses(self): 
        #Consultas
        self.cur.execute('select * from MAIN_BONUSES where BONUS_ID=%s and rownum<=1' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(self.cur);
        result=dict[0]
        fieldNames=dict[1]

        #Cantidad de registros actualizados
        self.assertEqual(len(result),1)

        for row in result:
            self.assertEqual(row[fieldNames['SITE_ID']],'MLA')
            self.assertEqual(row[fieldNames['CURRENCY_ID']],'u$s')


    def test5_update_on_feed_charges(self):
        #Consultas
        self.cur.execute('select * from FEED_CHARGES where CHARGE_ID=%s and rownum<=2' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(self.cur);
        result=dict[0]
        fieldNames=dict[1]
            
        #Cantidad de registros insertados
        self.assertEqual(len(result),2)

         #Valores actualizados
        for row in result:
            self.assertEqual(row[fieldNames['TYPE']],'B')
    
    def test6_delete_loaded_data(self):
        #Delete test 
        try:
            self.cur.execute('delete from CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from MAIN_BONUSES where BONUS_ID = %s' % (self.chargeId))
            self.cur.execute('delete from FEED_CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from PMS where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from SYI_ORDER where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from OTHER_MAIN_CHARGES_DATA where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from CHARGES_ERRORS where CHARGE_ID = %s' % (self.chargeId))
            self.db.commit()
            self.assertTrue(1,1)  
        except ValueError:
            self.assertTrue(1,2)

    def tearDown(self):
        #Close connection
        self.db.commit()
        self.cur.close() 
        self.db.close()

if __name__ == '__main__':
    #Init test fw
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)

   

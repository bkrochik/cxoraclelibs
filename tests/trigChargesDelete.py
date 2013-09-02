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
        self.cur.execute("INSERT INTO CHARGES (CURRENCY_ID,SITE_ID,CHARGE_TYPE_ID,DOC_ID,CHARGE_ID,CUST_ID,CATEG_ID,ITEM_ID,QUANTITY,UNIT_PRICE,CHARGE_DT,CHARGE_STATUS,PAY_STATUS,INS_DT,REF_CHARGE_ID,BID_CUST_ID,PAY_AMOUNT,BID_SEQUENCE,CUST_SITE,ORIG_CURRENCY,DOL_UNIT_PRICE,ORIG_UNIT_PRICE,ORIG_ITEM_UNIT_PRICE,FROM_PRG,ORIG_ITEM_CURRENCY,FROM_USER,COMMENTS,BONIF_STATUS,COLLECTED_AMOUNT,MAIL_BONIF,PREPAY,AFF_SITE_CHARGE,AFF_PYMNT_CHARGE,TIMESTAMP,QTY_BONIF,AFF_CHARGE_PRICE,SEARCH_WORD,COMBO_TYPE_ID) VALUES ('MEX','MLM','CV',358008,4112095,10003446,'1832',3534564,1,0.97,TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),'F','T',TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),NULL,NULL,0.97,1,'MLM','DOL',0.1,0.1,0.1,NULL,'DOL',NULL,NULL,NULL,NULL,NULL,NULL,219639,11552,TO_DATE('03-JUL-2006 11:23:26','DD-MON-RRRR HH24:MI:SS'),0,0.97,NULL,NULL)")
        self.db.commit()
        #Obtengo el id del insertado
        self.cur.execute('select * from CHARGES where rownum<=1 order by TIMESTAMP desc')
       
        #Armo diccionario de datos
        dict=self.createDict(self.cur);
        result=dict[0]
        fieldNames=dict[1]
        
        for row in result:
            self.chargeId=row[fieldNames['CHARGE_ID']]
          
    
    def test1_delete_loaded_data(self):
        #Delete test 
        try:
            self.cur.execute('delete from CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from MAIN_CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from FEED_CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from PMS where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from SYI_ORDER where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from OTHER_MAIN_CHARGES_DATA where CHARGE_ID = %s' % (self.chargeId))
            self.db.commit()
            
            #Obtengo el id del insertado
            self.cur.execute('select * from CHARGES_ERRORS where rownum<=1 and CHARGE_ID = %s' % (self.chargeId))
            
            #Armo diccionario de datos
            dict=self.createDict(self.cur);
            result=dict[0]

            #Cantidad de registros insertados por error
            self.assertEqual(len(result),1)

            #Borro logs de error
            self.cur.execute('delete from CHARGES_ERRORS where CHARGE_ID = %s' % (self.chargeId))
            self.db.commit()
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
   
   

   

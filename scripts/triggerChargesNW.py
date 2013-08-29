import random
import unittest
import cx_Oracle

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        #Setting connection TNS
        ip = '10.0.10.26'
        port = 1521
        SID = 'desa11g'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        self.db = cx_Oracle.connect('billing', 'GHaURU13', dsn_tns)
        #Insert test data
        cur=self.db.cursor()
        #cur.execute("INSERT INTO CHARGES (CURRENCY_ID,SITE_ID,CHARGE_TYPE_ID,DOC_ID,CHARGE_ID,CUST_ID,CATEG_ID,ITEM_ID,QUANTITY,UNIT_PRICE,CHARGE_DT,CHARGE_STATUS,PAY_STATUS,INS_DT,REF_CHARGE_ID,BID_CUST_ID,PAY_AMOUNT,BID_SEQUENCE,CUST_SITE,ORIG_CURRENCY,DOL_UNIT_PRICE,ORIG_UNIT_PRICE,ORIG_ITEM_UNIT_PRICE,FROM_PRG,ORIG_ITEM_CURRENCY,FROM_USER,COMMENTS,BONIF_STATUS,COLLECTED_AMOUNT,MAIL_BONIF,PREPAY,AFF_SITE_CHARGE,AFF_PYMNT_CHARGE,TIMESTAMP,QTY_BONIF,AFF_CHARGE_PRICE,SEARCH_WORD,COMBO_TYPE_ID) VALUES ('MEX','MLM','CV',358008,4112094,10003446,'1832',3534564,1,0.97,TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),'F','T',TO_DATE('13-AUG-2002 21:47:37','DD-MON-RRRR HH24:MI:SS'),NULL,NULL,0.97,1,'MLM','DOL',0.1,0.1,0.1,NULL,'DOL',NULL,NULL,NULL,NULL,NULL,NULL,219639,11552,TO_DATE('03-JUL-2006 11:23:26','DD-MON-RRRR HH24:MI:SS'),0,0.97,NULL,NULL)")
        #cur.commit()
        #Obtengo el id del insertado
        cur.execute('select charge_id from CHARGES where rownum=1 order by TIMESTAMP desc')
        resultset = cur.fetchall()
        self.idToDelete=168#resultset[0][0]

    def test_query(self):
        cur = self.db.cursor()
        #Consultas
        cur.execute('select * from MAIN_CHARGES where CHARGE_ID='+str(self.idToDelete)+' and rownum=1')
        resultset = cur.fetchall()
        for result in resultset:
            self.assertEqual(168,result[0])
        #Registros insertados
        self.assertEqual(len(resultset),1)
        
    def test_insert(self):
        cur=self.db.cursor()
        #Example insert 1) .execute(INSERTQUERY) 2) .commit()
        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()

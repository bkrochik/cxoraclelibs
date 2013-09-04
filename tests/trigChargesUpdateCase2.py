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

        #Update
        self.cur.execute("UPDATE CHARGES SET SITE_ID='MLA',ITEM_ID=123,AFF_PYMNT_CHARGE='123',ORIG_CURRENCY='TST',CHARGE_TYPE_ID='BV' WHERE CHARGE_ID=4112095")
        self.db.commit()

        #Set data
        self.chargeId=4112095
        self.siteId='MLA'
        self.itemId='123'
        self.marketplace='BV'
        self.affPymntCharge='123'
        self.origCurrency='TST'

    def test1_update_on_main_charges(self): 
        #Consultas
        self.cur.execute('select * from MAIN_CHARGES where CHARGE_ID=%s and rownum<=1' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(self.cur);
        result=dict[0]
        fieldNames=dict[1]

        #Cantidad de registros actualizados
        self.assertEqual(len(result),1)

        for row in result:
            self.assertEqual(row[fieldNames['SITE_ID']],'MLA')

    def test2_update_on_syi_order(self):
        #Consultas
        self.cur.execute('select * from SYI_ORDER where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
        
        if self.itemId != None or self.quantity != None or self.unitPrice != None:      
            #Armo diccionario de datos
            dict=self.createDict(self.cur);
            result=dict[0]
            fieldNames=dict[1]
            
            #Cantidad de registros actualizados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['ITEM_ID']],123)
        else:
            #Cantidad de registros insertados
            self.assertEqual(len(self.cur.fetchall()),0)

    def test3_update_on_pms(self):
        #Consultas
        self.cur.execute('select * from PMS where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
     
        if self.affPymntCharge != None or self.affSiteCharge != None or self.affChargePrice != None:

            #Armo diccionario de datos
            dict=self.createDict(self.cur);
            result=dict[0]
            fieldNames=dict[1]
            
            #Cantidad de registros actualizados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['AFF_PYMNT_CHARGE']],123)

        else:
            #Cantidad de registros insertados
            self.assertEqual(len(self.cur.fetchall()),0)

    def test4_update_on_other_main_charges_data(self):
        #Consultas
        self.cur.execute('select * from OTHER_MAIN_CHARGES_DATA where CHARGE_ID=%s and rownum<=1' % (self.chargeId))
     
        if self.origCurrency != None or self.oringUnitPrice != None or self.origItemCurrency != None or self.origItemUnitPrice != None or self.collectedAmount != None:
            #Armo diccionario de datos
            dict=self.createDict(self.cur);
            result=dict[0]
            fieldNames=dict[1]

            #Cantidad de registros actualizados
            self.assertEqual(len(result),1)

            #Valores insertados
            for row in result:
                self.assertEqual(row[fieldNames['ORIG_CURRENCY']],'TST')

        else:
            #Cantidad de registros insertados
            self.assertEqual(len(self.cur.fetchall()),0)

    def test5_update_on_feed_charges(self):
        #Consultas
        self.cur.execute('select * from FEED_CHARGES where CHARGE_ID=%s and rownum<=1' % (self.chargeId))

        #Armo diccionario de datos
        dict=self.createDict(self.cur);
        result=dict[0]
        fieldNames=dict[1]
            
        #Cantidad de registros insertados
        self.assertEqual(len(result),1)

         #Valores actualizados
        for row in result:
            self.assertEqual(row[fieldNames['TYPE']],'C')
    
    def test6_delete_loaded_data(self):
        #Delete test 
        try:
            self.cur.execute('delete from CHARGES where CHARGE_ID = %s' % (self.chargeId))
            self.cur.execute('delete from MAIN_CHARGES where CHARGE_ID = %s' % (self.chargeId))
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

   

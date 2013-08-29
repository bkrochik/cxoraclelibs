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


    def test_query(self):
        cur = self.db.cursor()
        #Consultas
        cur.execute('select * from feed_charges where rownum=1')
        resultset = cur.fetchall()
        for result in resultset:
            self.assertEqual(168,result[0])
        
    def test_insert(self):
        cur=self.db.cursor()
        #Example insert 1) .execute(INSERTQUERY) 2) .commit()
        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()

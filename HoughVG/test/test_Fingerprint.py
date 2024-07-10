import unittest
from HoughVG import Fingerprint
import time
Template_Path_Big='./images/Big_DB'
DataBase_path_Big='./images/Big_data_minuties'#Database_test

Template_Path_Little='./images/little_DB'
DataBase_path_Little='./images/little_data_minuties'#Database_test

class TestFingerprint_Big_DB(unittest.TestCase):
    def test_fingerprint(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        start = time.time()
        Fingerprint.fingerprint(Template_Path_Big,DataBase_path_Big,seuil_long,seuil_larg,seuil_rot)
        #print('resultats=', results)
        end = time.time()
        print("Sequentiel(Big DB):exécution time(en secondes): %f" %float( end - start)) 

    def test_fingerprintP(self):
        n_cpu=2
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        start = time.time()
        Fingerprint.fingerprintP(Template_Path_Big,DataBase_path_Big,seuil_long,seuil_larg,seuil_rot,n_cpu)
        #print('resultats=', results)
        end = time.time()
        print("Parallel(Big DB):exécution time(en secondes): %f" %float( end - start)) 

class TestFingerprint_little_DB(unittest.TestCase):
    def test_fingerprint(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        start = time.time()
        Fingerprint.fingerprint(Template_Path_Little,DataBase_path_Little,seuil_long,seuil_larg,seuil_rot)
        #print('resultats=', results)
        end = time.time()
        print("Sequentiel (little DB):exécution time(en secondes): %f" %float( end - start)) 

    def test_fingerprintP(self):
        n_cpu=2
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        start = time.time()
        Fingerprint.fingerprintP(Template_Path_Little,DataBase_path_Little,seuil_long,seuil_larg,seuil_rot,n_cpu)
        #print('resultats=', results)
        end = time.time()
        print("Parallel (little DB):exécution time(en secondes): %f" %float( end - start)) 

if __name__ == '__main__':
    unittest.main()

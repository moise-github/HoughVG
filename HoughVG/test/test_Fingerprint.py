import unittest
from HoughVG import Fingerprint
import time
Template_Path_Big='./images/Big_DB'
DataBase_path_Big='./images/fingerprint_2'#Database_test

Template_Path_Little='./images/little_DB'
DataBase_path_Little='./images/fingerprint_1'#Database_test

class TestFingerprint_Big_DB(unittest.TestCase):
    def test_fingerprint(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        Sc=3
        precision=0
        start = time.time()
        Fingerprint.fingerprint(Template_Path_Big,DataBase_path_Big,seuil_long,seuil_larg,seuil_rot,Sc,precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintSequentialBigDB.txt','w') as f:
            print("Sequential(Big DB):exécution time(s): %f" %float( end - start), file=f) 

    def test_fingerprintVG(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        Sc=3
        precision=0
        start = time.time()
        Fingerprint.fingerprint_VG(Template_Path_Big,DataBase_path_Big,seuil_long,seuil_larg,seuil_rot,Sc,precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintVGBigDB.txt','w') as f:
            print("Virtual Grid(Big DB):exécution time(s): %f" %float( end - start),file=f) 


    def test_fingerprintVGP(self):
        n_cpu=2
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        Sc=3
        precision=0
        start = time.time()
        Fingerprint.fingerprint_VGP(Template_Path_Big,DataBase_path_Big,seuil_long,seuil_larg,seuil_rot,Sc,n_cpu, precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintHybridBigDB.txt','w') as f:
            print("Hybrid(Big DB):exécution time(s): %f" %float( end - start),file=f) 

class TestFingerprint_little_DB(unittest.TestCase):
    def test_fingerprint(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        precision=0
        Sc=3
        start = time.time()
        Fingerprint.fingerprint(Template_Path_Little,DataBase_path_Little,seuil_long,seuil_larg,seuil_rot,Sc,precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintSequentialLittleDB.txt','w') as f:
            print("Sequentiel (little DB):exécution time(s): %f" %float( end - start),file=f) 

    def test_fingerprintVG(self):
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        precision=0
        Sc=3
        start = time.time()
        Fingerprint.fingerprint_VG(Template_Path_Little,DataBase_path_Little,seuil_long,seuil_larg,seuil_rot,Sc,precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintVGLittleDB.txt','w') as f:
            print("Virtual Grid (little DB):exécution time(s): %f" %float( end - start),file=f) 


    def test_fingerprintVGP(self):
        n_cpu=2
        seuil_long=10
        seuil_larg=10
        seuil_rot=5
        precision=0
        Sc=3
        start = time.time()
        Fingerprint.fingerprint_VGP(Template_Path_Little,DataBase_path_Little,seuil_long,seuil_larg,seuil_rot,Sc,n_cpu,precision)
        #print('resultats=', results)
        end = time.time()
        with open('../results/FingerprintHybridLittleDB.txt','w') as f:
            print("Hybrid (little DB):exécution time(s): %f" %float( end - start),file=f) 

if __name__ == '__main__':
    unittest.main()

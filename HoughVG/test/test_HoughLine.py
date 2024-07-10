import unittest
from HoughVG import HoughLine
import cv2
import time
imge_auto = cv2.imread('./images/autoroute2.jpg')
imge_Build = cv2.imread('./images/univ.png')
def ImgPreprocessing(imge,EdgesThresholdMin, EdgesThresholdMax):
    img = cv2.Canny(imge, EdgesThresholdMin, EdgesThresholdMax, None, 3)
    return img

class TestHoughLine_Road(unittest.TestCase):
    def test_Standard(self):
        colors=(0, 255, 0)
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Standard(img,Threshold)
        t2=time.time()
        T=t2-t1
        print('THS_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')

        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THS_road_accum_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THS_road_accum_max_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THS_road_lines_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Rectangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        l=3
        L=3
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Rectangular(img,l,L,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THR_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')

        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)

        cv2.imwrite('./images/test_THR_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THR_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THR_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Triangular1(self):
        colors=(0, 255, 0)
        Rate=0.4
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Triangular1(img,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THT1_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THT1_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THT1_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THT1_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Triangular2(self):
        colors=(0, 255, 0)
        Rate=0.4
        h=3
        b=3
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Triangular2(img,h,b,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THT2_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THT2_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THT2_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THT2_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

        
    def test_hexagonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Hexagonal(img,gamma,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THH_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THH_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THH_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THH_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_octogonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Hexagonal(img,gamma,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THO_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THO_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THO_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THO_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)


class TestHoughLine_Building(unittest.TestCase):
    def test_Standard(self):
        colors=(0, 255, 0)
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        
        t1=time.time()
        accum, accum_max,lines= HoughLine.Standard(img,Threshold)
        t2=time.time()
        T=t2-t1
        print('THS_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')

        img2=HoughLine.PlotHoughLine(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THS_building_accum_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THS_building_accum_max_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THS_building_lines_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Rectangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        l=3
        L=3
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Rectangular(img,l,L,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THR_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THR_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THR_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THR_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Triangular1(self):
        colors=(0, 255, 0)
        Rate=0.4
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Triangular1(img,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THT1_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THT1_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THT1_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THT1_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Triangular2(self):
        colors=(0, 255, 0)
        Rate=0.4
        h=3
        b=3
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Triangular2(img,h,b,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THT2_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THT2_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THT2_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THT2_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

        
    def test_hexagonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLine.Hexagonal(img,gamma,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THH_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THH_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THH_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THH_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_octogonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLine.Octogonal(img,gamma,Rate,Threshold)
        t2=time.time()
        T=t2-t1
        print('THO_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLine.PlotHoughLine(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THO_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THO_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THO_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

if __name__ == '__main__':
    unittest.main()

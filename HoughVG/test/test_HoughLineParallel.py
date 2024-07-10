import unittest
from HoughVG import HoughLineParallel
import cv2
import time
imge_auto = cv2.imread('./images/autoroute2.jpg')
imge_Build = cv2.imread('./images/univ.png')
def ImgPreprocessing(imge,EdgesThresholdMin, EdgesThresholdMax):
    img = cv2.Canny(imge, EdgesThresholdMin, EdgesThresholdMax, None, 3)
    return img

class TestHoughLineParallel_Road(unittest.TestCase):
    def test_Rectangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        l=3
        L=3
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLineParallel.RectangularP(img,l,L,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THRP_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THRP_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THRP_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THRP_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)


    def test_Triangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        h=3
        b=3
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLineParallel.TriangularP(img,h,b,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THTP_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THTP_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THTP_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THTP_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

        
    def test_hexagonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLineParallel.HexagonalP(img,gamma,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THHP_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THHP_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THHP_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THHP_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_octogonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_auto,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLineParallel.OctogonalP(img,gamma,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THOP_road:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_auto,lines,colors)
        cv2.imwrite('./images/test_THOP_road_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THOP_road_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THOP_road_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)


class TestHoughLine_Building(unittest.TestCase):
    def test_Rectangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        l=3
        L=3
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max, lines= HoughLineParallel.RectangularP(img,l,L,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THRP_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THRP_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THRP_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THRP_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_l%02d'%l +'_L%02d'%L +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_Triangular(self):
        colors=(0, 255, 0)
        Rate=0.4
        h=3
        b=3
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLineParallel.TriangularP(img,h,b,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THTP_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THTP_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THTP_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THTP_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_h%02d'%h +'_b%02d'%b +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

        
    def test_hexagonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLineParallel.HexagonalP(img,gamma,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THHP_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THHP_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THHP_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THHP_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

    def test_octogonal(self):
        colors=(0, 255, 0)
        Rate=0.4
        gamma=2
        n_cpu=2
        Threshold=50
        EdgesThresholdMax=500
        EdgesThresholdMin=200
        img=ImgPreprocessing(imge_Build,EdgesThresholdMin, EdgesThresholdMax)
        cv2.imshow('Edges detection with Canny', img)
        t1=time.time()
        accum, accum_max,lines= HoughLineParallel.OctogonalP(img,gamma,Rate,Threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print('THOP_building:Lines detection time :', T, 'sec' )
        if T>=60 : print('soit :', int(T/60), 'min :',T%60, 'sec')
        img2=HoughLineParallel.PlotHoughLineP(imge_Build,lines,colors)
        cv2.imwrite('./images/test_THOP_Building_accum_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum)
        cv2.imwrite('./images/test_THOP_Building_accum_max_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', accum_max)
        cv2.imwrite('./images/test_THOP_Building_lines_Rate'+'%02d'%Rate +'_Threshold %02d'%Threshold +'_Gamma%02d'%gamma +'_CannyMin%02d'%EdgesThresholdMin +'_CannyMax%02d'%EdgesThresholdMax +'.png', img2)

if __name__ == '__main__':
    unittest.main()

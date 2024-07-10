import pymp
import scipy
import math
import time
import cv2 as cv 
import os
from math import sqrt
import numpy as np
import scipy.ndimage
from skimage.morphology import skeletonize as skelt
import tkinter as tk


def normalize_pixel(x, v0, v, m, m0):
    dev_coeff = sqrt((v0 * ((x - m)**2)) / v)
    return m0 + dev_coeff if x > m else m0 - dev_coeff

def normalize(im, m0, v0):
    #print('im.shape=',im.shape)
    m = np.mean(im)
    v = np.std(im) ** 2
    (y, x) = im.shape
    normilize_image = im.copy()
    for i in range(x):
        for j in range(y):
            normilize_image[j, i] = normalize_pixel(im[j, i], v0, v, m, m0)
   
    return normilize_image

def normalise(img):
    return (img - np.mean(img))/(np.std(img))

def create_segmented_and_variance_images(im, w, threshold): 
    (y, x) = im.shape
    threshold = np.std(im)*threshold
    image_variance = np.zeros(im.shape)
    segmented_image = im.copy()
    mask = np.ones_like(im)
    for i in range(0, x, w):
        for j in range(0, y, w):
            box = [i, j, min(i + w, x), min(j + w, y)]
            block_stddev = np.std(im[box[1]:box[3], box[0]:box[2]])
            image_variance[box[1]:box[3], box[0]:box[2]] = block_stddev
    # apply threshold
    mask[image_variance < threshold] = 0
    # smooth mask with a open/close morphological filter
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(w*2, w*2))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    # normalize segmented image
    segmented_image *= mask
    im = normalise(im)
    mean_val = np.mean(im[mask==0])
    std_val = np.std(im[mask==0])
    norm_img = (im - mean_val)/(std_val)
    return segmented_image, norm_img, mask

def calculate_angles(im, W, smoth=False):   
    j1 = lambda x, y: 2 * x * y
    j2 = lambda x, y: x ** 2 - y ** 2
    (y, x) = im.shape
    sobelOperator = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ySobel = np.array(sobelOperator).astype(np.int64)
    xSobel = np.transpose(ySobel).astype(np.int64)
    result = [[] for i in range(1, y, W)]
    Gx_ = cv.filter2D(im/125,-1, ySobel)*125
    Gy_ = cv.filter2D(im/125,-1, xSobel)*125
    for j in range(1, y, W):
        for i in range(1, x, W):
            nominator = 0
            denominator = 0
            for l in range(j, min(j + W, y - 1)):
                for k in range(i, min(i + W , x - 1)):
                    Gx = round(Gx_[l, k])  # horizontal gradients at l, k
                    Gy = round(Gy_[l, k])  # vertial gradients at l, k
                    nominator += j1(Gx, Gy)
                    denominator += j2(Gx, Gy)         
            if nominator or denominator:
                angle = (math.pi + math.atan2(nominator, denominator)) / 2
                result[int((j-1) // W)].append(angle)
            else:
                result[int((j-1) // W)].append(0)
    result = np.array(result)
    if smoth:
        result = smooth_angles(result)
    return result

def gauss(x, y):
    ssigma = 1.0
    return (1 / (2 * math.pi * ssigma)) * math.exp(-(x * x + y * y) / (2 * ssigma))

def kernel_from_function(size, f):
    kernel = [[] for i in range(0, size)]
    for i in range(0, size):
        for j in range(0, size): 
            kernel[i].append(f(i - size / 2, j - size / 2))
    return kernel

def smooth_angles(angles):
    angles = np.array(angles)
    cos_angles = np.cos(angles.copy()*2)
    sin_angles = np.sin(angles.copy()*2)
    kernel = np.array(kernel_from_function(5, gauss))
    cos_angles = cv.filter2D(cos_angles/125,-1, kernel)*125
    sin_angles = cv.filter2D(sin_angles/125,-1, kernel)*125
    smooth_angles = np.arctan2(sin_angles, cos_angles)/2
    return smooth_angles

def frequest(im, orientim, kernel_size, minWaveLength, maxWaveLength):    
    rows, cols = np.shape(im)  
    cosorient = np.cos(2*orientim) # np.mean(np.cos(2*orientim))
    sinorient = np.sin(2*orientim) # np.mean(np.sin(2*orientim))
    block_orient = math.atan2(sinorient,cosorient)/2   
    # Rotate the image block so that the ridges are vertical
    rotim = scipy.ndimage.rotate(im,block_orient/np.pi*180 + 90,axes=(1,0),reshape = False,order = 3,mode = 'nearest')
    # Now crop the image so that the rotated image does not contain any invalid regions.
    cropsze = int(np.fix(rows/np.sqrt(2)))
    offset = int(np.fix((rows-cropsze)/2))
    rotim = rotim[offset:offset+cropsze][:,offset:offset+cropsze]
    # Sum down the columns to get a projection of the grey values down the ridges.
    ridge_sum = np.sum(rotim, axis = 0)
    dilation = scipy.ndimage.grey_dilation(ridge_sum, kernel_size, structure=np.ones(kernel_size))
    ridge_noise = np.abs(dilation - ridge_sum); peak_thresh = 2;
    maxpts = (ridge_noise < peak_thresh) & (ridge_sum > np.mean(ridge_sum))
    maxind = np.where(maxpts)
    _, no_of_peaks = np.shape(maxind)   
    if(no_of_peaks<2):
        freq_block = np.zeros(im.shape)
    else:
        waveLength = (maxind[0][-1] - maxind[0][0])/(no_of_peaks - 1)
        if waveLength>=minWaveLength and waveLength<=maxWaveLength:
            freq_block = 1/np.double(waveLength) * np.ones(im.shape)
        else:
            freq_block = np.zeros(im.shape)
    return(freq_block)

def ridge_freq(im, mask, orient, block_size, kernel_size, minWaveLength, maxWaveLength):
    rows,cols = im.shape
    freq = np.zeros((rows,cols))
    #with pymp.Parallel(n_cpu) as p:
    for row in range(0, rows - block_size, block_size):
        for col in range(0, cols - block_size, block_size):
            image_block = im[row:row + block_size][:, col:col + block_size]
            angle_block = orient[row // block_size][col // block_size]
            if angle_block:
                freq[row:row + block_size][:, col:col + block_size] = frequest(image_block, angle_block, kernel_size, minWaveLength, maxWaveLength)
    freq = freq*mask
    freq_1d = np.reshape(freq,(1,rows*cols))
    ind = np.where(freq_1d>0)
    ind = np.array(ind)
    ind = ind[1,:]
    non_zero_elems_in_freq = freq_1d[0][ind]
    medianfreq = np.median(non_zero_elems_in_freq) * mask
    return medianfreq

def gabor_filter(im, orient, freq, kx=0.65, ky=0.65):
    angleInc = 3
    im = np.double(im)
    rows, cols = im.shape
    return_img = np.zeros((rows,cols))
    freq_1d = freq.flatten()
    frequency_ind = np.array(np.where(freq_1d>0))
    non_zero_elems_in_freq = freq_1d[frequency_ind]
    non_zero_elems_in_freq = np.double(np.round((non_zero_elems_in_freq*100)))/100
    unfreq = np.unique(non_zero_elems_in_freq)
    sigma_x = 1/unfreq*kx
    sigma_y = 1/unfreq*ky
    block_size = np.round(3*np.max([sigma_x,sigma_y]))
    array = np.linspace(-block_size,block_size,int((2*block_size + 1)))
    x, y = np.meshgrid(array, array)
    # gabor filter equation
    reffilter = np.exp(-(((np.power(x,2))/(sigma_x*sigma_x) + (np.power(y,2))/(sigma_y*sigma_y)))) * np.cos(2*np.pi*unfreq[0]*x)
    filt_rows, filt_cols = reffilter.shape
    gabor_filter = np.array(np.zeros((180//angleInc, filt_rows, filt_cols)))
    for degree in range(0,180//angleInc):
        rot_filt = scipy.ndimage.rotate(reffilter,-(degree*angleInc + 90),reshape = False)
        gabor_filter[degree] = rot_filt
    maxorientindex = np.round(180/angleInc)
    orientindex = np.round(orient/np.pi*180/angleInc)   
    for i in range(0,rows//16):
        for j in range(0,cols//16):
            if(orientindex[i][j] < 1):
                orientindex[i][j] = orientindex[i][j] + maxorientindex
            if(orientindex[i][j] > maxorientindex):
                orientindex[i][j] = orientindex[i][j] - maxorientindex
   
    block_size = int(block_size)
    valid_row, valid_col = np.where(freq>0)
    finalind = \
        np.where((valid_row>block_size) & (valid_row<rows - block_size) & (valid_col>block_size) & (valid_col<cols - block_size))
    for k in range(0, np.shape(finalind)[1]):
        r = valid_row[finalind[0][k]]; c = valid_col[finalind[0][k]]
        img_block = im[r-block_size:r+block_size + 1][:,c-block_size:c+block_size + 1]
        return_img[r][c] = np.sum(img_block * gabor_filter[int(orientindex[r//16][c//16]) - 1])
    gabor_img = 255 - np.array((return_img < 0)*255).astype(np.uint8)

    return gabor_img



def feature(img):
    features = []
    h, w = img.shape
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if img[i, j] == 0:  # Les points de pixels sont noirs
                m = i
                n = j
                eightField = [img[m - 1, n - 1], img[m - 1, n], img[m - 1, n + 1], img[m, n - 1], img[m, n + 1],
                              img[m + 1, n - 1], img[m + 1, n], img[m + 1, n + 1]]
              
                if sum(eightField) / 255 == 7:  #1 bloc noir, points d'extrémité

                    #  Déterminer si une image d'empreinte digitale est un bord
                    if sum(img[:i, j]) == 255 * i or sum(img[i + 1:, j]) == 255 * (w - i - 1) or sum(
                            img[i, :j]) == 255 * j or sum(img[i, j + 1:]) == 255 * (h - j - 1):
                             continue
                    canContinue=True
                    #print(m, n)
                    coordinate = [[m - 1, n - 1], [m - 1, n], [m - 1, n + 1], [m, n - 1], [m, n + 1], [m + 1, n - 1],
                                  [m + 1, n], [m + 1, n + 1]]
                    for o in range(8):  # Trouver le prochain point de connexion
                        if eightField[o] == 0:
                            index = o
                            m = coordinate[o][0]
                            n = coordinate[o][1]
                            # print(m, n, index)
                            break
                    # print(m, n, index)
                    for k in range(4):
                        coordinate = [[m - 1, n - 1], [m - 1, n], [m - 1, n + 1], [m, n - 1], [m, n + 1],
                                      [m + 1, n - 1], [m + 1, n], [m + 1, n + 1]]
                        eightField = [img[m - 1, n - 1], img[m - 1, n], img[m - 1, n + 1], img[m, n - 1], img[m, n + 1],
                                      img[m + 1, n - 1], img[m + 1, n], img[m + 1, n + 1]]
                        if sum(eightField) / 255 == 6:  # Points de connexion
                            for o in range(8):
                                if eightField[o] == 0 and o != 7 - index:
                                    index = o
                                    m = coordinate[o][0]
                                    n = coordinate[o][1]
                                    # print(m, n, index)
                                    break
                        else:
                            # print("false", i, j)
                            canContinue =False
                    if canContinue==True:

                        if n - j != 0:
                            if i - m >= 0 and j - n > 0:
                                direction = math.atan((i - m) / (n - j)) + math.pi
                            elif i - m < 0 and j - n > 0:
                                direction = math.atan((i - m) / (n - j)) - math.pi
                            else:
                                direction = math.atan((i - m) / (n - j))
                        else:
                            if i - m >= 0:
                                direction = math.pi / 2
                            else:
                                direction = -math.pi / 2
                        feature = []
                        feature.append(i)
                        feature.append(j)
                        feature.append(direction)
                        feature.append("endpoint")
                        features.append(feature)
                        
                        

                elif sum(eightField) / 255 == 5:  #3 blocs noirs, points de bifurcation
                    coordinate = [[m - 1, n - 1], [m - 1, n], [m - 1, n + 1], [m, n - 1], [m, n + 1], [m + 1, n - 1],
                                  [m + 1, n], [m + 1, n + 1]]
                    junctionCoordinates = []
                    junctions = []
                    canContinue =True
                    #  Éliminer les points de bifurcation non conformes
                    for o in range(8):  # Trouver le prochain point de connexion
                        if eightField[o] == 0:
                            junctions.append(o)
                            junctionCoordinates.append(coordinate[o])
                    for k in range(3):
                        if k == 0:
                            a = junctions[0]
                            b = junctions[1]
                        elif k == 1:
                            a = junctions[1]
                            b = junctions[2]
                        else:
                            a = junctions[0]
                            b = junctions[2]
                        if (a == 0 and b == 1) or (a == 1 and b == 2) or (a == 2 and b == 4) or (a == 4 and b == 7) or (
                                a == 6 and b == 7) or (a == 5 and b == 6) or (a == 3 and b == 5) or (a == 0 and b == 3):
                            canContinue =False
                            break

                    if canContinue==True:  # points de bifurcation qualifiés
                        canContinue =True
                        for k in range(3):  # Réalisé de trois manières
                            if canContinue==True:
                                junctionCoordinate = junctionCoordinates[k]
                                m = junctionCoordinate[0]
                                n = junctionCoordinate[1]
                                eightField = [img[m - 1, n - 1], img[m - 1, n], img[m - 1, n + 1], img[m, n - 1],
                                              img[m, n + 1],
                                              img[m + 1, n - 1], img[m + 1, n], img[m + 1, n + 1]]
                                coordinate = [[m - 1, n - 1], [m - 1, n], [m - 1, n + 1], [m, n - 1], [m, n + 1],
                                              [m + 1, n - 1], [m + 1, n], [m + 1, n + 1]]
                                canContinue =False
                                for o in range(8):
                                    if eightField[o] == 0:
                                        a = coordinate[o][0]
                                        b = coordinate[o][1]
                                        
                                        if (a != i or b != j) and (
                                                a != junctionCoordinates[0][0] or b != junctionCoordinates[0][1]) and (
                                                a != junctionCoordinates[1][0] or b != junctionCoordinates[1][1]) and (
                                                a != junctionCoordinates[2][0] or b != junctionCoordinates[2][1]):
                                            index = o
                                            m = a
                                            n = b
                                            canContinue =True
                                            break
                                if canContinue==True:  # Possibilité de trouver un deuxième point de branchement
                                    for p in range(3):
                                        coordinate = [[m - 1, n - 1], [m - 1, n], [m - 1, n + 1], [m, n - 1],
                                                      [m, n + 1],
                                                      [m + 1, n - 1], [m + 1, n], [m + 1, n + 1]]
                                        eightField = [img[m - 1, n - 1], img[m - 1, n], img[m - 1, n + 1],
                                                      img[m, n - 1],
                                                      img[m, n + 1],
                                                      img[m + 1, n - 1], img[m + 1, n], img[m + 1, n + 1]]
                                        if sum(eightField) / 255 == 6:  # Points de connexion
                                            for o in range(8):
                                                if eightField[o] == 0 and o != 7 - index:
                                                    index = o
                                                    m = coordinate[o][0]
                                                    n = coordinate[o][1]
                                                    break
                                        else:
                                            
                                            canContinue =False
                                if canContinue==True:  # Capable de trouver 3 connexions
                                    
                                    if n - j != 0:
                                        if i - m >= 0 and j - n > 0:
                                            direction = math.atan((i - m) / (n - j)) + math.pi
                                        elif i - m < 0 and j - n > 0:
                                            direction = math.atan((i - m) / (n - j)) - math.pi
                                        else:
                                            direction = math.atan((i - m) / (n - j))
                                    else:
                                        if i - m >= 0:
                                            direction = math.pi / 2
                                        else:
                                            direction = -math.pi / 2
                                    
                                    feature = []
                                    feature.append(i)
                                    feature.append(j)
                                    feature.append(direction)
                                    feature.append("bifurcation")
                                    features.append(feature)                     
    bifurc=[]
    bif=[]          
    for z in range(len(features)):
        if features[z][3] == "bifurcation":
            bifurc.append(features[z])

    for t in range(1,len(bifurc)):
        x1=bifurc[t-1][0]
        y1=bifurc[t-1][1]
        x2=bifurc[t][0]
        y2=bifurc[t][1]
        dist=sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))
        if dist>50:
            bif.append(bifurc[t])
            
    ending=[]
    end=[]          
    for z in range(len(features)):
        if features[z][3] == "ending":
            ending.append(features[z])

    for t in range(1,len(ending)):
        x1=ending[t-1][0]
        y1=ending[t-1][1]
        x2=ending[t][0]
        y2=ending[t][1]
        dist=sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))
        D=dist[0]
        dist=D[0]
        if dist>5:
            end.append(ending[t])
        
    Feat=[]
    for g in range(len(bif)):
        Feat.append(bif[g])
    for k in range(len(end)):
        Feat.append(end[k])
    
    for m in range(len(Feat)):
        if Feat[m][3] == "ending":
            cv.circle(img, (Feat[m][1], Feat[m][0]), 3, (255, 0, 255), 1)
        else:
            cv.circle(img, (Feat[m][1], Feat[m][0]), 3, (0, 0, 255), -1)
            
    return img ,Feat
def skeletonize(image_input):
  
    image = np.zeros_like(image_input)
    image[image_input == 0] = 1.0
    output = np.zeros_like(image_input)

    skeleton = skelt(image)
    output[skeleton] = 255
    cv.bitwise_not(output, output)

    return output

# Transformée de hough adaptée

def Hough_Transform(template1,template2,td_long,td_larg,tr):
    # Nombre de minuties dans les deux ensembles
    N=len(template1)
    M=len(template2)
    
    liste=[] # Liste pour stocker les paires de minuties correspondantes
    
    for i in range(N):
            for j in range(M):
                # Récupération des coordonnées et orientations des minuties
                tab1=template1[i]
                tab2=template2[j]
                theta1=tab1[2]
                theta2=float(tab2[2]) 
                x0=np.asarray(tab1[0])
                y0=np.asarray(tab1[1])
                x1=np.asarray(float(tab2[0]))
                y1=np.asarray(float(tab2[1]))

                # Conversion des angles en degrés
                theta1=math.degrees(theta1)
                theta2=math.degrees(theta2)

                # Calcul de la différence d'angle
                Delta_theta= min(abs(theta1-theta2),360-abs(theta1-theta2))
                Dx=x0-x1*math.cos(Delta_theta)-y1*math.sin(Delta_theta)
                Dy=y0+x1*math.sin(Delta_theta)-y1*math.cos(Delta_theta)
            
                Delta_theta=math.degrees(Delta_theta)

                # Vérification des conditions pour considérer une paire de minuties
                if (Dx>=0 and Dx<td_larg) and (Dy>=0 and Dy<td_long) and (Delta_theta<tr):
                    liste.append({i,j})

# Score de similarité
                  
    score=(len(liste)*len(liste))/(N*M)
         
    return score, liste
  

def fingerprint(Template_Path,DataBase_path,seuil_long,seuil_larg,seuil_rot):
    # Définition de la taille des blocs pour les images segmentées
    block_size = 16

    # Récupération du nombre de fichiers dans les répertoires de modèles et de base de données
    size2, = np.shape(os.listdir(Template_Path))
    size1, =np.shape(os.listdir(DataBase_path))

    # Initialisation des listes pour stocker les noms de fichiers
    Filename = [1]*size2 
    filename = [1]*size1 

    # Compteurs pour itérer sur les fichiers
    count1=0
    count2=0

    # Initialisation des scores pour chaque modèle
    score = [0]*size2
    
    # Chargement des noms de fichiers dans les listes correspondantes
    for file in os.listdir(DataBase_path):
        filename[count1]=file
        count1+=1
    for file in os.listdir(Template_Path):
        Filename[count2]=file
        count2+=1
    for i in range(size2):

        # Chargement et prétraitement de l'image modèle
        im= cv.imread(Template_Path+'/'+Filename[i],0)
        normalized_img = normalize(im,float(100),float(100)) # normalisation
        _, norm_img, mask=create_segmented_and_variance_images(normalized_img, block_size, 0.2)
        angles = calculate_angles(normalized_img, block_size, smoth=False)
        freq = ridge_freq(norm_img, mask, angles, block_size, kernel_size=5, minWaveLength=5, maxWaveLength=15)
        gabor_img = gabor_filter(norm_img, angles, freq)
        thin_image = skeletonize(gabor_img) # squeletisation
        _, minutiae1= feature(thin_image) # Extraction des minuties
        
        k=0  # Initialisation de la variable score

        # Comparaison des minuties 
        for j in range(size1):
            minutiae2 = np.load(DataBase_path+'/'+filename[j]).tolist()
            score[i],liste=Hough_Transform(minutiae1,minutiae2,seuil_long,seuil_larg,seuil_rot)
            if (score[i]>k):
                k=score[i]
            if (len(liste)>=10):
                b=b+1

        # Retourne le score maximum et un indicateur de correspondance
        if (k<0.7)  :
            return k, 0
        else:
            return k, 1
   


def fingerprintP(Template_Path,DataBase_path,seuil_long,seuil_larg,seuil_rot,n_cpu):
    # Activation du support pour les parallélismes imbriqués dans pymp
    pymp._config.nested=True

    # Définition de la taille des blocs pour les images segmentées
    block_size = 16

    # Récupération du nombre de fichiers dans les répertoires de modèles et de base de données
    size2, = np.shape(os.listdir(Template_Path))
    size1, =np.shape(os.listdir(DataBase_path))

    # Initialisation des listes pour stocker les noms de fichiers
    Filename = [1]*size2 
    filename = [1]*size1 

    # Compteurs pour itérer sur les fichiers
    count1=0
    count2=0

    # Initialisation des scores pour chaque modèle
    score = [0]*size2

    # Chargement des noms de fichiers dans les listes correspondantes
    for file in os.listdir(DataBase_path):
        filename[count1]=file
        count1+=1
    for file in os.listdir(Template_Path):
        Filename[count2]=file
        count2+=1

    # Liste partagée pour stocker les résultats de chaque thread
    results=pymp._shared.list([None]*n_cpu)

    # Démarrage du traitement parallèle
    with pymp.Parallel(n_cpu,if_=True) as p:
        for i in range(size2):

            # Chargement et prétraitement de l'image modèle
            im= cv.imread(Template_Path+'/'+Filename[i],0)
            normalized_img = normalize(im,float(100),float(100)) # normalisation
            _, norm_img, mask=create_segmented_and_variance_images(normalized_img, block_size, 0.2)
            angles = calculate_angles(normalized_img, block_size, smoth=False)
            freq = ridge_freq(norm_img, mask, angles, block_size, kernel_size=5, minWaveLength=5, maxWaveLength=15)
            gabor_img = gabor_filter(norm_img, angles, freq)
            thin_image = skeletonize(gabor_img) # squeletisation
            _, minutiae1 = feature(thin_image) # Extraction des minuties

            k=0 # Initialisation de la variable score

            # Comparaison des minuties 
            for j in p.range(size1):
                minutiae2 = np.load(DataBase_path+'/'+filename[j]).tolist()
                score[i],liste=Hough_Transform(minutiae1,minutiae2,seuil_long,seuil_larg,seuil_rot)
                if (score[i]>k):
                    k=score[i]
                
            # Stockage du meilleur score pour le thread courant
            results[p.thread_num]=k
    # Récupération des résultats finaux        
    Resultats=results
    k=max(Resultats)
    # Retourne le score maximum et un indicateur de correspondance
    if (k<0.7)  :
        return k, 0
        
    else:
        return k, 1
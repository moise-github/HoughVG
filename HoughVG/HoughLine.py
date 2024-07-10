import cv2
import numpy
import math
import matplotlib.pyplot as plt
from  matplotlib.pyplot import *

def maillage_oct(img, gamma):
    Ip = img.shape
    nl=Ip[0]
    nc=Ip[1]
    tab=[0, 0, 0, 0, 0]
    tab[0]= gamma
    tab[1]=round(nl/(3*gamma-2))
    tab[2]=round(nc/(3*gamma-2))
    tab[3]=nl%(3*gamma-2)
    tab[4]= nc%(3*gamma-2)   
    return tab

def comptage_oct(img, A, B, D, E, F, G, H, I, J):
    k=0
    l=0
    li=img.shape[0]
    ci=img.shape[1]
    for y in range(A[1], D[1]+1):
        if y in range(A[1], I[1]):          
            NP=abs(y-A[1])
            for x in range(A[0]-NP, H[0]+NP+1):
                if 0<=y<ci and 0<=x<li :
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
        if y in range(I[1], J[1]+1): 
            for x in range(B[0], G[0]+1):
                if 0<=y<ci and 0<=x<li :
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
        if y in range(J[1]+1, D[1]+1): 
            MQ=abs(y-D[1]-1)
            for x in range(D[0]-MQ+1, E[0]+MQ):
                if 0<=y<ci and 0<=x<li :
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
    taux=k/(k+l)
    return taux

def PrimEr(n):
    
    k = 2
    v = math.sqrt(n)
    e = round(v)
    while k <= e:
        r = n%k
        if r==0:
            return 0
        k = k+1
        
    return 1
#------------------------------------------------------------------------------#
def factorisation(n):
    """facteurs(n): décomposition d'un nombre entier n en facteurs premiers"""
    nf=n
    F = []
    if n==1:
        return F
    # recherche de tous les facteurs 2 s'il y en a
    while n>=2:
        x,r = divmod(n,2)
        if r!=0:
            break
        F.append(2)
        n = x
    # recherche des facteurs 1er >2
    i=3
    rn = round(n)+1
    while i<=n:
        if i>rn:
            F.append(n)
            break
        x,r = divmod(n,i)
        if r==0:
            F.append(i)
            n=x
            rn = round(n)+1
        else:
            i += 2
    k =round(len(F)/2)
    k2 = F[k]
    k1 = round(nf/k2)
    return k1, k2
#------------------------------------------------------------------------------#    
def maillage_tri1(img):
    Ip = img.shape
    nl=Ip[0]
    nc=Ip[1]
    tab=[0, 0, 0, 0, 0, 0]
    tab[4]=PrimEr(nl)
    if tab[4]==1:
        tab[0]=factorisation(nl-1)[0]
        tab[1]=factorisation(nl-1)[1]
    else:
        tab[0]=factorisation(nl)[0]
        tab[1]=factorisation(nl)[1]
    tab[5]=PrimEr(nc)
    if tab[5]==1:
        tab[2]=factorisation(nc-1)[0]
        tab[3]=factorisation(nc-1)[1]
    else:
        tab[2]=factorisation(nc)[0]
        tab[3]=factorisation(nc)[1]
   
    return tab
#-----------------------------------------------------------------------------#
def maillage_tri2(img, h, b):
    Ip = img.shape
    nl=Ip[0]
    nc=Ip[1]
    tab=[0, 0, 0, 0, 0, 0]
    tab[3]=h
    tab[1]=b
    tab[0]
    tab[2]
    tab[4]= nl%h
    tab[5]= nc%b
    return tab
        
def comptage_tri(img, A, B,C):
    k=0
    l=0
    D=[0, 0]
    D=A
    if B[1]>=A[1] and C[0]>=A[0]:
        for z in range(A[0], C[0]):
                   DE=round((abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)/(abs(C[0]-A[0])+1))
                   y0=A[1]+DE
                   for t in range(A[1], y0):
                       if img[z, t]!=0:
                          k=k+1
                       else:
                          l=l+1
    D=A
    if B[1]<=A[1] and C[0]<=A[0]: 
        for z in range(C[0], A[0]+1):
                   DE=(abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)//(abs(C[0]-A[0])+1)
                   y0=A[1]-DE+1
                   for t in range(y0, A[1]+1):
                       if img[z, t]!=0:
                          k=k+1
                       else:
                          l=l+1
    taux=k/(k+l)
    return taux

def maillage_Hex(img, gamma):
    Ip = img.shape
    nl=Ip[0]
    nc=Ip[1]
    tab=[0, 0, 0, 0, 0]
    tab[0]= gamma
    tab[1]=int(nl/(2*gamma-2))
    tab[2]=int(nc/(4*gamma-2))
    tab[3]=nl%(2*gamma-2)
    tab[4]= nc%(4*gamma-2)   
    return tab

def Rely(A, B):#fonction reliant les points A et B par une droite discrete. elle retourne une liste des pixels situe sur la dite droite.
    if A[0]==B[0]:
        L=abs(B[1]-A[1])
        MAT=[]
        for n in range(L-1):
            MAT.append((A[0], abs(B[1]-(n+1))))
    elif A[1]==B[1]:
        L=abs(B[0]-A[0])
        MAT=[]      
        for i in range(L-1):
            MAT.append((abs(B[0]-(i+1)), A[1]))
    else :
        L=abs(B[0]-A[0])
        MAT=[]
        if (B[1]>A[1]) and (B[0]>A[0]):           
            for n in range(L-1):   
                MAT.append((abs(B[0]-(n+1)), abs(B[1]-(n+1))))                                       
        elif(B[1]>A[1]) and (B[0]<A[0]):
            for n in range(L-1):  
                MAT.append((abs(A[0]-(n+1)), abs(A[1]+(n+1))))                                       
    return MAT

def comptage_Hex(img, A, B, C, D, E, F, G, H):
    k=0
    l=0
    li=img.shape[0]
    ci=img.shape[1]
    MAT1=Rely(A, F)
    MAT2=Rely(F, E)
    MAT3=Rely(E, D)
    for y in range(A[1], D[1]+1):
        if y in range(A[1], G[1]):          
            NP=abs(y-A[1])
            for x in range(A[0]-NP, A[0]+NP+1):
                if (x, y) in MAT1: 
                    continue
                if y<ci and x<li and x>=0 and y>=0:
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
        if y in range(G[1], H[1]+1): 
            for x in range(B[0], F[0]):
                if ((x, y) in MAT2) or (x, y)==(B[0], B[1]) or (x, y)== (C[0], C[1]):
                    continue
                if y<ci and x<li and x>=0 and y>=0:
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
        if y in range(H[1]+1, D[1]+1): 
            MQ=abs(y-D[1]-1)
            for x in range(A[0]-MQ, A[0]+MQ+1):
                if (x, y) in MAT3: 
                    continue
                if y<ci and x<li and x>=0 and y>=0:
                    if img[x, y]!=0:
                        k=k+1
                    else:
                        l=l+1
    if k!=0 and l!=0 :
        taux=k/(k+l)
    else:
        taux=0
    return taux

def maillage_rect(img, h1, b1):
    Ip = img.shape
    nl=Ip[0]
    nc=Ip[1]
    tab=[0, 0, 0, 0, 0, 0]
    tab[3]=h1
    tab[1]=b1
    tab[0]
    tab[2]
    tab[4]= nl%h1
    tab[5]= nc%b1
        
    return tab

def comptage_rect(img, A, B,D):
    k=0
    l=0
    for z in range(A[0], D[0]+1):
        for t in range(A[1], B[1]+1):
            if img[z, t]!=0:
                k=k+1
            else:
                l=l+1
    taux=k/(k+l)
    return taux
#------------------------------------------------------------------

def Standard(img,threshold):
        
        
        array=numpy.array(img)*1.0
        img_shape= array.shape
        Ny=img_shape[0]
        Nx=img_shape[1]
        
        rho= 1.0
        theta=1.0
        Ntheta = int(180.0/theta)
        Nrho = int(math.floor(math.sqrt(Nx*Nx+Ny*Ny))/rho)
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(Nx*Nx+Ny*Ny))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))
        # mise a jours de l'accumulateur
        for j in range(Ny):
            for i in range(Nx):
                if (array[j][i]!=0).any():
                    for i_theta in range(Ntheta):
                        theta = i_theta*dtheta
                        rho = i*math.cos(theta)+(Ny-j)*math.sin(theta)
                        i_rho = int(rho/drho)
                        if (i_rho>0) and (i_rho<Nrho):
                            accum[i_theta][i_rho] += 1

        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<threshold:
                    accum_seuil[i_theta][i_rho] = 0

        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))
        
        return accum, accum_seuil, lignes

def Rectangular(img,l,L,Rate,Threshold):       
        
        array=numpy.array(img)*1.0
        img_shape= array.shape
        Nl=img_shape[0] 
        Nc=img_shape[1] 
        tab = maillage_rect(img, l, L)
        H=Nl-tab[4]
        Lg=Nc-tab[5]
        H1=H+tab[3]
        L1=Lg+tab[1]
        ######### definition de l'accumulateur  #############
        A=[0, 0]
        B=[0, 0]
        D=[0, 0]
        Tau=10*Rate
        rho= 1.0
        theta=1.0
        Ntheta = int(180.0/theta) 
        Nrho = int(math.floor(math.sqrt(Nc*Nc+Nl*Nl))/rho)
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(Nc*Nc+Nl*Nl))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))
        
        ############# mise a jours de l'accumulateur ##################
        for x in range(tab[3]-1, H1-1, tab[3]):
            for y in range(tab[1]-1, L1-1, tab[1]): 
                A[0]=x-tab[3]+1
                A[1]=y-tab[1]+1
                B[0]=x-tab[3]+1
                B[1]=y
                D[0]=x
                D[1]=y-tab[1]+1
                if comptage_rect(img, A, B, D)>= Rate:
                    for z in range(A[0], D[0]+1):
                        for t in range(A[1], B[1]+1):
                            if (array[z][t]!=0).any():
                                for i_theta in range(Ntheta):
                                    theta = i_theta*dtheta
                                    rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                                    i_rho = int(rho/drho)
                                    if (i_rho>0) and (i_rho<Nrho):
                                        accum[i_theta][i_rho] += 1

        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<Threshold:
                    accum_seuil[i_theta][i_rho] = 0
                    
        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))
        return accum, accum_seuil, lignes         

def Hexagonal(img,gamma,rate,threshold):

        l=img.shape[0]
        c=img.shape[1]

        #      MAILLAGE        
        
        tab = maillage_Hex(img, gamma)
        Ht=l-tab[3]
        La=c-tab[4]
        H1=Ht+2*gamma-2
        L1=La+4*gamma-2
        #  definition de l'accumulateur
        Ntheta = 180
        Nrho = int(math.floor(math.sqrt(c*c+l*l)))
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(c*c+l*l))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))

        
        Rate=10*rate

        A=[0, 0]
        B=[0, 0]
        C=[0, 0]
        D=[0, 0]
        E=[0, 0]
        F=[0, 0]
        G=[0, 0]
        H=[0, 0]
        
        for y in range(3*gamma-2, L1, 4*gamma-2):
            for x in range(2*gamma-2, H1+1, 2*gamma-2): 
                A[0]=x-tab[0]+1
                A[1]=y-3*tab[0]+2
                B[0]=x-2*tab[0]+2
                B[1]=y-2*tab[0]+1
                C[0]=x-2*tab[0]+2
                C[1]=y-tab[0]+1
                D[0]=x-tab[0]+1
                D[1]=y
                E[0]=x
                E[1]=y-tab[0]+1
                F[0]=x
                F[1]=y-2*tab[0]+1
                G[0]=x-tab[0]+1
                G[1]=y-2*tab[0]+1
                H[0]=x-tab[0]+1
                H[1]=y-tab[0]+1

                if comptage_Hex(img, A, B, C, D, E, F, G, H)>= rate:
                    MAT1=Rely(A, F)
                    MAT2=Rely(F, E)
                    MAT3=Rely(E, D)
                    for j in range(A[1], D[1]+1):
                        if j in range(A[1], G[1]):                     
                            NP=abs(j-A[1])
                            for i in range(A[0]-NP, A[0]+NP+1):                       
                                if (i, j) in MAT1: 
                                    continue 
                                if j<c and i<l :                          
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1

                        if j in range(G[1], H[1]+1):
                            for i in range(B[0], F[0]):
                                if ((i, j) in MAT2) or (i, j)==(B[0], B[1]) or (i, j)== (C[0], C[1]):
                                    continue 
                                if j<c and i<l :
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1
                        
                        if j in range(H[1]+1, D[1]+1):                    
                            MQ=abs(j-D[1])
                            for i in range(A[0]-MQ, A[0]+MQ+1):
                                if (i, j) in MAT3: 
                                    continue
                                if j<c and i<l :
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1
        #####################################################
        for y in range(gamma-1, L1, 4*gamma-2):
            for x in range(gamma-1, H1, 2*gamma-2): 
                A[0]=x-tab[0]+1
                A[1]=y-3*tab[0]+2
                B[0]=x-2*tab[0]+2
                B[1]=y-2*tab[0]+1
                C[0]=x-2*tab[0]+2
                C[1]=y-tab[0]+1
                D[0]=x-tab[0]+1
                D[1]=y
                E[0]=x
                E[1]=y-tab[0]+1
                F[0]=x
                F[1]=y-2*tab[0]+1
                G[0]=x-tab[0]+1
                G[1]=y-2*tab[0]+1
                H[0]=x-tab[0]+1
                H[1]=y-tab[0]+1

                if comptage_Hex(img, A, B, C, D, E, F, G, H)>= rate:
                    MAT1=Rely(A, F)
                    MAT2=Rely(F, E)
                    MAT3=Rely(E, D)
                    for j in range(A[1], D[1]+1):
                        if j in range(A[1], G[1]):                     
                            NP=abs(j-A[1])
                            for i in range(A[0]-NP, A[0]+NP+1):                       
                                if (i, j) in MAT1: 
                                    continue  
                                if j<c and i<l and i>=0 and j>=0:                         
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1

                        if j in range(G[1], H[1]+1):
                            for i in range(B[0], F[0]):
                                if ((i, j) in MAT2) or (i, j)==(B[0], B[1]) or (i, j)== (C[0], C[1]):
                                    continue 
                                if j<c and i<l and i>=0 and j>=0:
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1
                        
                        if j in range(H[1]+1, D[1]+1):                    
                            MQ=abs(j-D[1])
                            for i in range(A[0]-MQ, A[0]+MQ+1):
                                if (i, j) in MAT3: 
                                    continue
                                if j<c and i<l and i>=0 and j>=0:
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1

        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<threshold:
                    accum_seuil[i_theta][i_rho] = 0

        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))

        return accum, accum_seuil, lignes

def Triangular1(img,Rate,Threshold):

        array=numpy.array(img)*1.0
        img_shape= array.shape
        Nl=img_shape[0] 
        Nc=img_shape[1] 
        tab = maillage_tri1(img)
        h=Nl-1 
        l=Nc-1
        ######### definition de l'accumulateur  #############
        A=[0,0] 
        B=[0,0]
        C=[0, 0]
       
        
        Tau=10*Rate
        rho= 1.0
        theta=1.0
        Ntheta = int(180.0/theta) 
        Nrho = int(math.floor(math.sqrt(Nc*Nc+Nl*Nl))/rho) 
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(Nc*Nc+Nl*Nl))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))
        ############# mise a jours de l'accumulateur ##################
        for x in range(tab[3]-1, Nl, tab[3]):
            for y in range(tab[1]-1, Nc, tab[1]): 
                A[0]=x-tab[3]+1
                A[1]=y-tab[1]+1
                B[0]=x-tab[3]+1
                B[1]=y
                C[0]=x
                C[1]=y-tab[1]+1
                D=A
                if B[1]>=A[1] and C[0]>=A[0]:
                    if comptage_tri(img, A, B, C)>= Rate:
                        for z in range(A[0], C[0]):
                            DE=math.floor((abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)/(abs(C[0]-A[0])+1))
                            y0=A[1]+DE
                            for t in range(A[1], y0):                
                                if (array[z][t]!=0).any():
                                    for i_theta in range(Ntheta):
                                        theta = i_theta*dtheta
                                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                                        i_rho = int(rho/drho)
                                        if (i_rho>0) and (i_rho<Nrho):
                                            accum[i_theta][i_rho] += 1
                                            
                A[0]=x
                A[1]=y
                C[0]=x-tab[3]+1
                C[1]=y
                B[0]=x
                B[1]=y-tab[1]+1
                D=A
                if B[1]<=A[1] and C[0]<=A[0]:
                    if comptage_tri(img, A, B, C)>= Rate:
                        for z in range(C[0], A[0]+1):
                            DE=(abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)//(abs(C[0]-A[0])+1)
                            y0=A[1]-DE+1
                            for t in range(y0, A[1]+1):                   
                                if (array[z][t]!=0).any():
                                    for i_theta in range(Ntheta):
                                        theta = i_theta*dtheta
                                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                                        i_rho = int(rho/drho)
                                        if (i_rho>0) and (i_rho<Nrho):
                                            accum[i_theta][i_rho] += 1
                                
        ######################## traitement des residus  ########################
        if tab[4]==1 and tab[5]==0:
            z=h
            for t in range(0,Nc):
                
                if (array[z][t]!=0).any():
                    for i_theta in range(Ntheta):
                        theta = i_theta*dtheta
                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                        i_rho = int(rho/drho)
                        if (i_rho>0) and (i_rho<Nrho):
                            accum[i_theta][i_rho] += 1
                        
        if tab[4]==0 and tab[5]==1:
            t=l
            for z in range(0,Nl):
                
                if (array[z][t]!=0).any():
                    for i_theta in range(Ntheta):
                        theta = i_theta*dtheta
                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                        i_rho = int(rho/drho)
                        if (i_rho>0) and (i_rho<Nrho):
                            accum[i_theta][i_rho] += 1   
                                    
        if tab[4]==1 and tab[5]==1:
            z=h
            for t in range(0,Nc):
                
                if (array[z][t]!=0).any():
                    for i_theta in range(Ntheta):
                        theta = i_theta*dtheta
                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                        i_rho = int(rho/drho)
                        if (i_rho>0) and (i_rho<Nrho):
                            accum[i_theta][i_rho] += 1   
        t=l
        for z in range(0,Nl):
            if (array[z][t]!=0).any():
                for i_theta in range(Ntheta):
                    theta = i_theta*dtheta
                    rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                    i_rho = int(rho/drho)
                    if (i_rho>0) and (i_rho<Nrho):
                        accum[i_theta][i_rho] += 1   
        ######################  traitement des residus fin ######################      

        # on retient le valeur de l'accumulateur au dessus du Seuil
        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<Threshold:
                    accum_seuil[i_theta][i_rho] = 0
                    
        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))
    
        return accum, accum_seuil, lignes

def Triangular2(img,h,b,Rate,Threshold):

        array=numpy.array(img)*1.0
        img_shape= array.shape
        Nl=img_shape[0] 
        Nc=img_shape[1] 
        tab = maillage_tri2(img, h, b)
        H=Nl-tab[4]
        L=Nc-tab[5]
        ######### definition de l'accumulateur  #############
        A=[0, 0]
        B=[0, 0]
        C=[0, 0]
        Tau=10*Rate
        rho= 1.0
        theta=1.0
        Ntheta = int(180.0/theta) 
        Nrho = int(math.floor(math.sqrt(Nc*Nc+Nl*Nl))/rho)
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(Nc*Nc+Nl*Nl))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))
        ############# mise a jours de l'accumulateur ##################
        for x in range(tab[3]-1, Nl, tab[3]):
            for y in range(tab[1]-1, Nc, tab[1]): 
                A[0]=x-tab[3]+1
                A[1]=y-tab[1]+1
                B[0]=x-tab[3]+1
                B[1]=y
                C[0]=x
                C[1]=y-tab[1]+1
                D=A
                if B[1]>=A[1] and C[0]>=A[0]:
                    if comptage_tri(img, A, B, C)>= Rate:
                        for z in range(A[0], C[0]):
                            DE=math.floor((abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)/(abs(C[0]-A[0])+1))
                            y0=A[1]+DE
                            for t in range(A[1], y0):
                                if (array[z][t]!=0).any():
                                    for i_theta in range(Ntheta):
                                        theta = i_theta*dtheta
                                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                                        i_rho = int(rho/drho)
                                        if (i_rho>0) and (i_rho<Nrho):
                                            accum[i_theta][i_rho] += 1
                                            
                A[0]=x
                A[1]=y
                C[0]=x-tab[3]+1
                C[1]=y
                B[0]=x
                B[1]=y-tab[1]+1
                D=A
                if B[1]<=A[1] and C[0]<=A[0]:
                    if comptage_tri(img, A, B, C)>= Rate:
                        for z in range(C[0], A[0]+1):
                            DE=(abs(C[0]-z)+1)*(abs(B[1]-A[1])+1)//(abs(C[0]-A[0])+1)
                            y0=A[1]-DE+1
                            for t in range(y0, A[1]+1):
                                if (array[z][t]!=0).any():
                                    for i_theta in range(Ntheta):
                                        theta = i_theta*dtheta
                                        rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                                        i_rho = int(rho/drho)
                                        if (i_rho>0) and (i_rho<Nrho):
                                            accum[i_theta][i_rho] += 1
                            
        ######################## traitement des residus  ########################
        if tab[4]!=0:
            for z in range(H, Nl):
                for t in range(0,Nc):
                
                    if (array[z][t]!=0).any():
                        for i_theta in range(Ntheta):
                            theta = i_theta*dtheta
                            rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                            i_rho = int(rho/drho)
                            if (i_rho>0) and (i_rho<Nrho):
                                accum[i_theta][i_rho] += 1
                        
        if tab[5]!=0:
            for z in range(0, Nl):
                for t in range(L, Nc):
                
                    if (array[z][t]!=0).any():
                        for i_theta in range(Ntheta):
                            theta = i_theta*dtheta
                            rho = t*math.cos(theta)+(Nl-z)*math.sin(theta)
                            i_rho = int(rho/drho)
                            if (i_rho>0) and (i_rho<Nrho):
                                accum[i_theta][i_rho] += 1
                                    
        ######################  traitement des residus fin ###################### 
        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<Threshold:
                    accum_seuil[i_theta][i_rho] = 0
                    
        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))
        
        return accum, accum_seuil, lignes

def Octogonal(img,gamma,Rate,Threshold):
        
        l=img.shape[0]
        c=img.shape[1]

        #      MAILLAGE        
        
        tab = maillage_oct(img, gamma)
        Ht=l-tab[3]
        La=c-tab[4]
        H1=Ht+3*gamma-2
        L1=La+3*gamma-2
        #  definition de l'accumulateur
        Ntheta = 180
        Nrho = int(math.floor(math.sqrt(c*c+l*l)))
        dtheta = math.pi/Ntheta
        drho = math.floor(math.sqrt(c*c+l*l))/Nrho
        accum = numpy.zeros((Ntheta,Nrho))

        Tau=10*Rate

        A=[0, 0]
        B=[0, 0]
        C=[0, 0]
        D=[0, 0]
        E=[0, 0]
        F=[0, 0]
        G=[0, 0]
        H=[0, 0]
        I=[0, 0]
        J=[0, 0]
        K=[0, 0]
        L=[0, 0]

        for y in range(3*gamma-2, L1, 3*gamma-1):
            for x in range(3*gamma-2, H1, 3*gamma-1): 
                A[0]=x-2*tab[0]+1
                A[1]=y-3*tab[0]+2
                B[0]=x-3*tab[0]+2
                B[1]=y-2*tab[0]+1
                C[0]=x-3*tab[0]+2
                C[1]=y-tab[0]+1
                D[0]=x-2*tab[0]+1
                D[1]=y
                E[0]=x-tab[0]+1
                E[1]=y
                F[0]=x
                F[1]=y-tab[0]+1
                G[0]=x
                G[1]=y-2*tab[0]+1
                H[0]=x-tab[0]+1
                H[1]=y-3*tab[0]+2
                I[0]=x-2*tab[0]+1
                I[1]=y-2*tab[0]+1
                J[0]=x-2*tab[0]+1
                J[1]=y-tab[0]+1
                K[0]=x-tab[0]+1
                K[1]=y-tab[0]+1
                L[0]=x-tab[0]+1
                L[1]=y-2*tab[0]+1
        ##########################################################################################
                if comptage_oct(img, A, B, D, E, F, G, H, I, J)>= Rate:
                    for j in range(A[1], D[1]+1):
                        if j in range(A[1], I[1]):                     
                            NP=abs(j-A[1])
                            for i in range(A[0]-NP, H[0]+NP+1):  
                                if 0<=j<c and 0<=i<l :                                              
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1

                        if j in range(I[1], J[1]+1):
                            for i in range(B[0], G[0]+1):                               
                                if 0<=j<c and 0<=i<l :  
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1
                        
                        if j in range(J[1]+1, D[1]+1):                    
                            MQ=abs(j-D[1]-1)
                            for i in range(D[0]-MQ+1, E[0]+MQ):
                                if 0<=j<c and 0<=i<l : 
                                    if (img[i][j]!=0).any():
                                        for i_theta in range(Ntheta):
                                            theta = i_theta*dtheta
                                            rho = j*math.cos(theta)+(l-i)*math.sin(theta)
                                            i_rho = int(rho/drho)
                                            if (i_rho>0) and (i_rho<Nrho):
                                                accum[i_theta][i_rho] += 1
        
        ###################################################################################################################                                 
        accum_seuil = accum.copy()
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum[i_theta][i_rho]<Threshold:
                    accum_seuil[i_theta][i_rho] = 0

        lignes = []
        for i_theta in range(Ntheta):
            for i_rho in range(Nrho):
                if accum_seuil[i_theta][i_rho]!=0:
                    lignes.append((i_rho*drho,i_theta*dtheta))
        
        return accum, accum_seuil, lignes

def PlotHoughLine(imge,lines,colors):
    img2 = imge.copy()     
    img_shape = imge.shape
    Ny = img_shape[0]
    Nx = img_shape[1]
    le=len(lines)

    for rho, theta in lines:
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a*rho
        y0 = b*rho
        pt1 = (int(x0 + 10000 * (-b)), Ny-int(y0 + 10000 * (a)))
        pt2 = (int(x0 - 10000 * (-b)), Ny-int(y0 - 10000 * (a)))
        cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
        
    return img2
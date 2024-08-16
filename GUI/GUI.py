import cv2
import math
import numpy as np
from tkinter import Tk, Label, Entry, Button, Scale, HORIZONTAL, filedialog, Radiobutton, IntVar
from PIL import Image, ImageTk
from HoughVG import HoughLine
from HoughVG import HoughLineParallel
from HoughVG import Fingerprint
import time
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class HoughVGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HoughVG")

        self.root.geometry("1360x640")  # Set the predefined size of the root window (width x height)

        self.root.configure(bg='#2E2E2E')  # Set the background color of the root window

        self.display_width=500
        self.display_height=400

        self.original_label = Label(root, bg='#2E2E2E')
        self.original_label.pack(side="left")

        self.processed_label = Label(root, bg='#2E2E2E')
        self.processed_label.pack(side="right")

        # Define dimensions for the buttons
        button_width = 40
        button_height = 1

        self.upload_button = Button(root, text="Charger une image", command=self.upload_image, width=button_width, height=button_height, bg='#4F4F4F', fg='#FFFFFF')
        self.upload_button.pack()

        self.upload_fingerprint_button=Button(root,text="Test",command=self.upload_Test_fingerprints, width=button_width, height=button_height, bg='#4F4F4F', fg='#FFFFFF')
        self.upload_fingerprint_button.pack()
        

        self.upload_BD_button=Button(root,text="BD",command=self.upload_BD_fingerprints, width=button_width, height=button_height, bg='#4F4F4F', fg='#FFFFFF')
        self.upload_BD_button.pack()

        self.process_fingerprint_button=Button(root,text="Identification",command=self.THG_fingerprint, width=button_width, height=button_height, bg='#4F4F4F', fg='#FFFFFF')
        self.process_fingerprint_button.pack()

        #Button to save the processed image
        self.save_button=Button(root,text="Sauvegarder", command=self.save_image, width=button_width, height=button_height, bg='#4F4F4F', fg='#FFFFFF')
        self.save_button.pack()

        # Radio buttons for main method
        self.main_method_var = IntVar()
        self.main_method_var.set(1)  # Default to Lines Detection
        self.lines_detection_radio = Radiobutton(root, text="Détection de droites", variable=self.main_method_var, value=1, command=self.select_main_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        self.lines_detection_radio.pack()
        self.fingerprint_detection_radio = Radiobutton(root, text="Reconnaissance d'empreintes digitales", variable=self.main_method_var, value=2, command=self.select_main_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        self.fingerprint_detection_radio.pack()


        # Radio buttons for method selection sequentiel
        self.method_var = IntVar()
        self.THR_line_method_radio = Radiobutton(root, text="Transformée de Hough Rectangulaire", variable=self.method_var, value=1, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THR_line_method_radio.pack()

        self.THT_line_method_radio = Radiobutton(root, text="Transformée de Hough Triangulaire", variable=self.method_var, value=2, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THT_line_method_radio.pack()

        self.THH_line_method_radio = Radiobutton(root, text="Transformée de Hough Hexagonale", variable=self.method_var, value=3, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THH_line_method_radio.pack()

        self.THO_line_method_radio = Radiobutton(root, text="Transformée de Hough Octogonale", variable=self.method_var, value=4, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THO_line_method_radio.pack()

        self.fingerprint_radio = Radiobutton(root, text="Identification d'empreintes", variable=self.method_var, value=5, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.fingerprint_radio.pack()

        # Radio buttons for method selection parallèle
        self.THRP_line_method_radio = Radiobutton(root, text="Transformée de Hough Rectangulaire Parallélisée", variable=self.method_var, value=6, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THRP_line_method_radio.pack()

        self.THTP_line_method_radio = Radiobutton(root, text="Transformée de Hough Triangulaire Parallélisée", variable=self.method_var, value=7, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THTP_line_method_radio.pack()

        self.THHP_line_method_radio = Radiobutton(root, text="Transformée de Hough Hexagonale Parallélisée", variable=self.method_var, value=8, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THHP_line_method_radio.pack()

        self.THOP_line_method_radio = Radiobutton(root, text="Transformée de Hough Octogonale Parallélisée", variable=self.method_var, value=9, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.THOP_line_method_radio.pack()

        self.fingerprintP_radio = Radiobutton(root, text="Identification d'empreintes Parallélisée ", variable=self.method_var, value=10, command=self.select_method, width=button_width, height=button_height, bg='#2E2E2E', fg='#FFFFFF', selectcolor='#4F4F4F')
        #self.fingerprintP_radio.pack()

        # Sliders for THR Line parameters
        self.line_THR_threshold_label = Label(root, text="THR Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THR_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THR_Rate_label = Label(root, text="THR alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THR_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THR_L_label = Label(root, text="THR longeur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THR_L_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THR_l_label = Label(root, text="THR largeur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THR_l_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THT Line parameters
        self.line_THT_threshold_label = Label(root, text="THT Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THT_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THT_Rate_label = Label(root, text="THT alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THT_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THT_h_label = Label(root, text="THT hauteur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THT_h_slider = Scale(root, from_=2, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THT_b_label = Label(root, text="THT base:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THT_b_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THH Line parameters
        self.line_THH_threshold_label = Label(root, text="THH Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THH_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THH_Rate_label = Label(root, text="THH alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THH_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THH_gamma_label = Label(root, text="THH Gamma:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THH_gamma_slider = Scale(root, from_=2, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THO Line parameters
        self.line_THO_threshold_label = Label(root, text="THO Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THO_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THO_Rate_label = Label(root, text="THO alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THO_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THO_gamma_label = Label(root, text="THO Gamma:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THO_gamma_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')
        ################################PARALLELE###############################""""""
        # Sliders for THRP Line parameters
        self.line_THRP_threshold_label = Label(root, text="THRP Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THRP_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THRP_Rate_label = Label(root, text="THRP alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THRP_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THRP_L_label = Label(root, text="THRP longeur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THRP_L_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THRP_l_label = Label(root, text="THRP largeur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THRP_l_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THTP Line parameters
        self.line_THTP_threshold_label = Label(root, text="THTP Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THTP_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THTP_Rate_label = Label(root, text="THTP alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THTP_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THTP_h_label = Label(root, text="THTP hauteur:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THTP_h_slider = Scale(root, from_=2, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THTP_b_label = Label(root, text="THTP base:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THTP_b_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THHP Line parameters
        self.line_THHP_threshold_label = Label(root, text="THHP Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THHP_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THHP_Rate_label = Label(root, text="THHP alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THHP_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THHP_gamma_label = Label(root, text="THHP Gamma:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THHP_gamma_slider = Scale(root, from_=2, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Sliders for THOP Line parameters
        self.line_THOP_threshold_label = Label(root, text="THOP Seuil de vote:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THOP_threshold_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THOP_Rate_label = Label(root, text="THOP alpha:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THOP_Rate_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.line_THOP_gamma_label = Label(root, text="THOP Gamma:", bg='#2E2E2E', fg='#FFFFFF')
        self.line_THOP_gamma_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        self.n_cpu_label = Label(root, text="Nombre de processus:", bg='#2E2E2E', fg='#FFFFFF')
        self.n_cpu_slider = Scale(root, from_=1, to=os.cpu_count(), orient=HORIZONTAL, command=self.update_detection, bg='#6E6E6E', fg='#000000', troughcolor='#4F4F4F')

        # Label to display identification of fingerprints
        self.identification_message_label = Label(root, text="", bg='#4F4F4F', fg='#FFFFFF')
        self.identification_message_label.pack()

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.DB_directory=None
        self.fingerprint_directory=None
        

        # Initially hide all sliders and set default method
        self.hide_all_sliders()
        self.selected_method = "THR"

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_threshold_slider
        self.line_THR_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THR_threshold_slider)
        self.line_THR_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THR_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_Rate_slider
        self.line_THR_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THR_Rate_slider)
        self.line_THR_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THR_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_L_slider
        self.line_THR_L_slider.bind('<FocusIn>', self.activer_raccourcis_line_THR_L_slider)
        self.line_THR_L_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THR_L_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_l_slider
        self.line_THR_l_slider.bind('<FocusIn>', self.activer_raccourcis_line_THR_l_slider)
        self.line_THR_l_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THR_l_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_threshold_slider
        self.line_THT_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THT_threshold_slider)
        self.line_THT_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THT_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_Rate_slider
        self.line_THT_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THT_Rate_slider)
        self.line_THT_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THT_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_b_slider
        self.line_THT_b_slider.bind('<FocusIn>', self.activer_raccourcis_line_THT_b_slider)
        self.line_THT_b_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THT_b_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_h_slider
        self.line_THT_h_slider.bind('<FocusIn>', self.activer_raccourcis_line_THT_h_slider)
        self.line_THT_h_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THT_h_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_threshold_slider
        self.line_THH_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THH_threshold_slider)
        self.line_THH_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THH_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_Rate_slider
        self.line_THH_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THH_Rate_slider)
        self.line_THH_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THH_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_gamma_slider
        self.line_THH_gamma_slider.bind('<FocusIn>', self.activer_raccourcis_line_THH_gamma_slider)
        self.line_THH_gamma_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THH_gamma_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_threshold_slider
        self.line_THO_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THO_threshold_slider)
        self.line_THO_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THO_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_Rate_slider
        self.line_THO_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THO_Rate_slider)
        self.line_THO_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THO_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_gamma_slider
        self.line_THO_gamma_slider.bind('<FocusIn>', self.activer_raccourcis_line_THO_gamma_slider)
        self.line_THO_gamma_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THO_gamma_slider.bind('<Button-1>', self.donner_focus)
######################################PARALLELE###################################
        self.n_cpu_slider.bind('<FocusIn>', self.activer_raccourcis_n_cpu_slider)
        self.n_cpu_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.n_cpu_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THRP_threshold_slider
        self.line_THRP_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THRP_threshold_slider)
        self.line_THRP_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THRP_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THRP_Rate_slider
        self.line_THRP_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THRP_Rate_slider)
        self.line_THRP_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THRP_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THRP_L_slider
        self.line_THRP_L_slider.bind('<FocusIn>', self.activer_raccourcis_line_THRP_L_slider)
        self.line_THRP_L_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THRP_L_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THRP_l_slider
        self.line_THRP_l_slider.bind('<FocusIn>', self.activer_raccourcis_line_THRP_l_slider)
        self.line_THRP_l_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THRP_l_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THTP_threshold_slider
        self.line_THTP_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THTP_threshold_slider)
        self.line_THTP_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THTP_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THTP_Rate_slider
        self.line_THTP_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THTP_Rate_slider)
        self.line_THTP_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THTP_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THTP_b_slider
        self.line_THTP_b_slider.bind('<FocusIn>', self.activer_raccourcis_line_THTP_b_slider)
        self.line_THTP_b_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THTP_b_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THTP_h_slider
        self.line_THTP_h_slider.bind('<FocusIn>', self.activer_raccourcis_line_THTP_h_slider)
        self.line_THTP_h_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THTP_h_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THHP_threshold_slider
        self.line_THHP_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THHP_threshold_slider)
        self.line_THHP_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THHP_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THHP_Rate_slider
        self.line_THHP_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THHP_Rate_slider)
        self.line_THHP_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THHP_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THHP_gamma_slider
        self.line_THHP_gamma_slider.bind('<FocusIn>', self.activer_raccourcis_line_THHP_gamma_slider)
        self.line_THHP_gamma_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THHP_gamma_slider.bind('<Button-1>', self.donner_focus)

        #associer les touches fléchées aux fonctions de déplacement du curseur line_THOP_threshold_slider
        self.line_THOP_threshold_slider.bind('<FocusIn>', self.activer_raccourcis_line_THOP_threshold_slider)
        self.line_THOP_threshold_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THOP_threshold_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THOP_Rate_slider
        self.line_THOP_Rate_slider.bind('<FocusIn>', self.activer_raccourcis_line_THOP_Rate_slider)
        self.line_THOP_Rate_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THOP_Rate_slider.bind('<Button-1>', self.donner_focus)
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THOP_gamma_slider
        self.line_THOP_gamma_slider.bind('<FocusIn>', self.activer_raccourcis_line_THOP_gamma_slider)
        self.line_THOP_gamma_slider.bind('<FocusOut>', self.desactiver_raccourcis)
        self.line_THOP_gamma_slider.bind('<Button-1>', self.donner_focus)
###########################################################################################""######
    def activer_raccourcis_line_THR_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THR_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THR_threshold_slider)
    def activer_raccourcis_line_THR_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THR_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THR_Rate_slider)
    def activer_raccourcis_line_THR_L_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_L_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THR_L_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THR_L_slider)
    def activer_raccourcis_line_THR_l_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_l_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THR_l_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THR_l_slider)

    def activer_raccourcis_line_THT_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THT_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THT_threshold_slider)
    def activer_raccourcis_line_THT_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THT_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THT_Rate_slider)
    def activer_raccourcis_line_THT_b_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_b_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THT_b_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THT_b_slider)
    def activer_raccourcis_line_THT_h_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_h_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THT_h_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THT_h_slider)

    def activer_raccourcis_line_THH_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THH_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THH_threshold_slider)
    def activer_raccourcis_line_THH_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THH_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THH_Rate_slider)
    def activer_raccourcis_line_THH_gamma_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_gamma_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THH_gamma_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THH_gamma_slider)

    def activer_raccourcis_line_THO_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THO_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THO_threshold_slider)
    def activer_raccourcis_line_THO_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THO_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THO_Rate_slider)
    def activer_raccourcis_line_THO_gamma_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_gamma_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THO_gamma_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THO_gamma_slider)

########################parallèle#####################################################"
    def activer_raccourcis_n_cpu_slider(self, event):
        self.root.bind('<Left>', self.deplacer_gauche_n_cpu_slider)
        self.root.bind('<Right>', self.deplacer_droite_n_cpu_slider)

    def activer_raccourcis_line_THRP_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THRP_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THRP_threshold_slider)
    def activer_raccourcis_line_THRP_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THRP_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THRP_Rate_slider)
    def activer_raccourcis_line_THRP_L_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_L_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THRP_L_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THRP_L_slider)
    def activer_raccourcis_line_THRP_l_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THR_l_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THRP_l_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THRP_l_slider)

    def activer_raccourcis_line_THTP_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THTP_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THTP_threshold_slider)
    def activer_raccourcis_line_THTP_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THTP_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THTP_Rate_slider)
    def activer_raccourcis_line_THTP_b_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_b_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THTP_b_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THTP_b_slider)
    def activer_raccourcis_line_THTP_h_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THT_h_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THTP_h_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THTP_h_slider)

    def activer_raccourcis_line_THHP_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THHP_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THHP_threshold_slider)
    def activer_raccourcis_line_THHP_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THHP_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THHP_Rate_slider)
    def activer_raccourcis_line_THHP_gamma_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THH_gamma_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THHP_gamma_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THHP_gamma_slider)

    def activer_raccourcis_line_THOP_threshold_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_threshold_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THOP_threshold_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THOP_threshold_slider)
    def activer_raccourcis_line_THOP_Rate_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_Rate_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THOP_Rate_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THOP_Rate_slider)
    def activer_raccourcis_line_THOP_gamma_slider(self, event):
        #associer les touches fléchées aux fonctions de déplacement du curseur line_THO_gamma_slider
        self.root.bind('<Left>', self.deplacer_gauche_line_THOP_gamma_slider)
        self.root.bind('<Right>', self.deplacer_droite_line_THOP_gamma_slider)
#####################################################################################
    def desactiver_raccourcis(self, event):
        #desactiver les touches fléchées des fonctions de déplacement
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
###########################################################################
    def deplacer_gauche_line_THR_threshold_slider(self,event):
        #deplacer le curseur line_THR_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THR_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THR_threshold_slider.cget('from'):
            self.line_THR_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THR_threshold_slider(self,event):
        #deplacer le curseur line_THR_threshold_slider vers la droite
        nouvelle_valeur=self.line_THR_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THR_threshold_slider.cget('to'):
            self.line_THR_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THR_Rate_slider(self,event):
        #deplacer le curseur line_THR_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THR_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THR_Rate_slider.cget('from'):
            self.line_THR_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THR_Rate_slider(self,event):
        #deplacer le curseur line_THR_Rate_slider vers la droite
        nouvelle_valeur=self.line_THR_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THR_Rate_slider.cget('to'):
            self.line_THR_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THR_L_slider(self,event):
        #deplacer le curseur line_THR_L_slider vers la gauche
        nouvelle_valeur=self.line_THR_L_slider.get()-1
        if nouvelle_valeur>=self.line_THR_L_slider.cget('from'):
            self.line_THR_L_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THR_L_slider(self,event):
        #deplacer le curseur line_THR_L_slider vers la droite
        nouvelle_valeur=self.line_THR_L_slider.get()+1
        if nouvelle_valeur<=self.line_THR_L_slider.cget('to'):
            self.line_THR_L_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THR_l_slider(self,event):
        #deplacer le curseur line_THR_l_slider vers la gauche
        nouvelle_valeur=self.line_THR_l_slider.get()-1
        if nouvelle_valeur>=self.line_THR_l_slider.cget('from'):
            self.line_THR_l_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THR_l_slider(self,event):
        #deplacer le curseur line_THR_l_slider vers la droite
        nouvelle_valeur=self.line_THR_l_slider.get()+1
        if nouvelle_valeur<=self.line_THR_l_slider.cget('to'):
            self.line_THR_l_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THT_threshold_slider(self,event):
        #deplacer le curseur line_THT_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THT_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THT_threshold_slider.cget('from'):
            self.line_THT_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THT_threshold_slider(self,event):
        #deplacer le curseur line_THT_threshold_slider vers la droite
        nouvelle_valeur=self.line_THT_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THT_threshold_slider.cget('to'):
            self.line_THT_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THT_Rate_slider(self,event):
        #deplacer le curseur line_THT_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THT_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THT_Rate_slider.cget('from'):
            self.line_THT_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THT_Rate_slider(self,event):
        #deplacer le curseur line_THT_Rate_slider vers la droite
        nouvelle_valeur=self.line_THT_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THT_Rate_slider.cget('to'):
            self.line_THT_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THT_b_slider(self,event):
        #deplacer le curseur line_THT_b_slider vers la gauche
        nouvelle_valeur=self.line_THT_b_slider.get()-1
        if nouvelle_valeur>=self.line_THT_b_slider.cget('from'):
            self.line_THT_b_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THT_b_slider(self,event):
        #deplacer le curseur line_THT_L_slider vers la droite
        nouvelle_valeur=self.line_THT_b_slider.get()+1
        if nouvelle_valeur<=self.line_THT_b_slider.cget('to'):
            self.line_THT_b_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THT_h_slider(self,event):
        #deplacer le curseur line_THT_h_slider vers la gauche
        nouvelle_valeur=self.line_THT_h_slider.get()-1
        if nouvelle_valeur>=self.line_THT_h_slider.cget('from'):
            self.line_THT_h_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THT_h_slider(self,event):
        #deplacer le curseur line_THT_h_slider vers la droite
        nouvelle_valeur=self.line_THT_h_slider.get()+1
        if nouvelle_valeur<=self.line_THT_h_slider.cget('to'):
            self.line_THT_h_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THH_threshold_slider(self,event):
        #deplacer le curseur line_THH_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THH_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THH_threshold_slider.cget('from'):
            self.line_THH_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THH_threshold_slider(self,event):
        #deplacer le curseur line_THH_threshold_slider vers la droite
        nouvelle_valeur=self.line_THH_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THH_threshold_slider.cget('to'):
            self.line_THH_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THH_Rate_slider(self,event):
        #deplacer le curseur line_THH_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THH_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THH_Rate_slider.cget('from'):
            self.line_THH_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THH_Rate_slider(self,event):
        #deplacer le curseur line_THH_Rate_slider vers la droite
        nouvelle_valeur=self.line_THH_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THH_Rate_slider.cget('to'):
            self.line_THH_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THH_gamma_slider(self,event):
        #deplacer le curseur line_THH_gamma_slider vers la gauche
        nouvelle_valeur=self.line_THH_gamma_slider.get()-1
        if nouvelle_valeur>=self.line_THH_gamma_slider.cget('from'):
            self.line_THH_gamma_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THH_gamma_slider(self,event):
        #deplacer le curseur line_THH_gamma_slider vers la droite
        nouvelle_valeur=self.line_THH_gamma_slider.get()+1
        if nouvelle_valeur<=self.line_THH_gamma_slider.cget('to'):
            self.line_THH_gamma_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THO_threshold_slider(self,event):
        #deplacer le curseur line_THO_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THO_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THO_threshold_slider.cget('from'):
            self.line_THO_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THO_threshold_slider(self,event):
        #deplacer le curseur line_THO_threshold_slider vers la droite
        nouvelle_valeur=self.line_THO_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THO_threshold_slider.cget('to'):
            self.line_THO_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THO_Rate_slider(self,event):
        #deplacer le curseur line_THO_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THO_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THO_Rate_slider.cget('from'):
            self.line_THO_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THO_Rate_slider(self,event):
        #deplacer le curseur line_THO_Rate_slider vers la droite
        nouvelle_valeur=self.line_THO_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THO_Rate_slider.cget('to'):
            self.line_THO_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THO_gamma_slider(self,event):
        #deplacer le curseur line_THO_gamma_slider vers la gauche
        nouvelle_valeur=self.line_THO_gamma_slider.get()-1
        if nouvelle_valeur>=self.line_THO_gamma_slider.cget('from'):
            self.line_THO_gamma_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THO_gamma_slider(self,event):
        #deplacer le curseur line_THO_gamma_slider vers la droite
        nouvelle_valeur=self.line_THO_gamma_slider.get()+1
        if nouvelle_valeur<=self.line_THO_gamma_slider.cget('to'):
            self.line_THO_gamma_slider.set(nouvelle_valeur)
################################PARALLÈLE################################""
    def deplacer_gauche_n_cpu_slider(self,event):
        #deplacer le curseur line_THRP_threshold_slider vers la gauche
        nouvelle_valeur=self.n_cpu_slider.get()-1
        if nouvelle_valeur>=self.n_cpu_slider.cget('from'):
            self.n_cpu_slider.set(nouvelle_valeur)
    def deplacer_droite_n_cpu_slider(self,event):
        #deplacer le curseur line_THRP_threshold_slider vers la droite
        nouvelle_valeur=self.n_cpu_slider.get()+1
        if nouvelle_valeur<=self.n_cpu_slider.cget('to'):
            self.n_cpu_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THRP_threshold_slider(self,event):
        #deplacer le curseur line_THRP_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THRP_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THRP_threshold_slider.cget('from'):
            self.line_THRP_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THRP_threshold_slider(self,event):
        #deplacer le curseur line_THRP_threshold_slider vers la droite
        nouvelle_valeur=self.line_THRP_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THRP_threshold_slider.cget('to'):
            self.line_THRP_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THRP_Rate_slider(self,event):
        #deplacer le curseur line_THRP_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THRP_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THRP_Rate_slider.cget('from'):
            self.line_THRP_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THRP_Rate_slider(self,event):
        #deplacer le curseur line_THRP_Rate_slider vers la droite
        nouvelle_valeur=self.line_THRP_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THRP_Rate_slider.cget('to'):
            self.line_THRP_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THRP_L_slider(self,event):
        #deplacer le curseur line_THRP_L_slider vers la gauche
        nouvelle_valeur=self.line_THRP_L_slider.get()-1
        if nouvelle_valeur>=self.line_THRP_L_slider.cget('from'):
            self.line_THRP_L_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THRP_L_slider(self,event):
        #deplacer le curseur line_THRP_L_slider vers la droite
        nouvelle_valeur=self.line_THRP_L_slider.get()+1
        if nouvelle_valeur<=self.line_THRP_L_slider.cget('to'):
            self.line_THRP_L_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THRP_l_slider(self,event):
        #deplacer le curseur line_THRP_l_slider vers la gauche
        nouvelle_valeur=self.line_THRP_l_slider.get()-1
        if nouvelle_valeur>=self.line_THRP_l_slider.cget('from'):
            self.line_THRP_l_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THRP_l_slider(self,event):
        #deplacer le curseur line_THRP_l_slider vers la droite
        nouvelle_valeur=self.line_THRP_l_slider.get()+1
        if nouvelle_valeur<=self.line_THRP_l_slider.cget('to'):
            self.line_THRP_l_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THTP_threshold_slider(self,event):
        #deplacer le curseur line_THTP_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THTP_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THTP_threshold_slider.cget('from'):
            self.line_THTP_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THTP_threshold_slider(self,event):
        #deplacer le curseur line_THTP_threshold_slider vers la droite
        nouvelle_valeur=self.line_THTP_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THTP_threshold_slider.cget('to'):
            self.line_THTP_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THTP_Rate_slider(self,event):
        #deplacer le curseur line_THTP_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THTP_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THTP_Rate_slider.cget('from'):
            self.line_THTP_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THTP_Rate_slider(self,event):
        #deplacer le curseur line_THTP_Rate_slider vers la droite
        nouvelle_valeur=self.line_THTP_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THTP_Rate_slider.cget('to'):
            self.line_THTP_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THTP_b_slider(self,event):
        #deplacer le curseur line_THTP_b_slider vers la gauche
        nouvelle_valeur=self.line_THTP_b_slider.get()-1
        if nouvelle_valeur>=self.line_THTP_b_slider.cget('from'):
            self.line_THTP_b_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THTP_b_slider(self,event):
        #deplacer le curseur line_THTP_L_slider vers la droite
        nouvelle_valeur=self.line_THTP_b_slider.get()+1
        if nouvelle_valeur<=self.line_THTP_b_slider.cget('to'):
            self.line_THTP_b_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THTP_h_slider(self,event):
        #deplacer le curseur line_THTP_h_slider vers la gauche
        nouvelle_valeur=self.line_THTP_h_slider.get()-1
        if nouvelle_valeur>=self.line_THTP_h_slider.cget('from'):
            self.line_THTP_h_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THTP_h_slider(self,event):
        #deplacer le curseur line_THTP_h_slider vers la droite
        nouvelle_valeur=self.line_THTP_h_slider.get()+1
        if nouvelle_valeur<=self.line_THTP_h_slider.cget('to'):
            self.line_THTP_h_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THHP_threshold_slider(self,event):
        #deplacer le curseur line_THHP_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THHP_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THHP_threshold_slider.cget('from'):
            self.line_THHP_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THHP_threshold_slider(self,event):
        #deplacer le curseur line_THHP_threshold_slider vers la droite
        nouvelle_valeur=self.line_THHP_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THHP_threshold_slider.cget('to'):
            self.line_THHP_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THHP_Rate_slider(self,event):
        #deplacer le curseur line_THHP_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THHP_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THHP_Rate_slider.cget('from'):
            self.line_THHP_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THHP_Rate_slider(self,event):
        #deplacer le curseur line_THHP_Rate_slider vers la droite
        nouvelle_valeur=self.line_THHP_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THHP_Rate_slider.cget('to'):
            self.line_THHP_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THHP_gamma_slider(self,event):
        #deplacer le curseur line_THHP_gamma_slider vers la gauche
        nouvelle_valeur=self.line_THHP_gamma_slider.get()-1
        if nouvelle_valeur>=self.line_THHP_gamma_slider.cget('from'):
            self.line_THHP_gamma_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THHP_gamma_slider(self,event):
        #deplacer le curseur line_THHP_gamma_slider vers la droite
        nouvelle_valeur=self.line_THHP_gamma_slider.get()+1
        if nouvelle_valeur<=self.line_THHP_gamma_slider.cget('to'):
            self.line_THHP_gamma_slider.set(nouvelle_valeur)

    def deplacer_gauche_line_THOP_threshold_slider(self,event):
        #deplacer le curseur line_THOP_threshold_slider vers la gauche
        nouvelle_valeur=self.line_THOP_threshold_slider.get()-1
        if nouvelle_valeur>=self.line_THOP_threshold_slider.cget('from'):
            self.line_THOP_threshold_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THOP_threshold_slider(self,event):
        #deplacer le curseur line_THOP_threshold_slider vers la droite
        nouvelle_valeur=self.line_THOP_threshold_slider.get()+1
        if nouvelle_valeur<=self.line_THOP_threshold_slider.cget('to'):
            self.line_THOP_threshold_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THOP_Rate_slider(self,event):
        #deplacer le curseur line_THOP_Rate_slider vers la gauche
        nouvelle_valeur=self.line_THOP_Rate_slider.get()-1
        if nouvelle_valeur>=self.line_THOP_Rate_slider.cget('from'):
            self.line_THOP_Rate_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THOP_Rate_slider(self,event):
        #deplacer le curseur line_THOP_Rate_slider vers la droite
        nouvelle_valeur=self.line_THOP_Rate_slider.get()+1
        if nouvelle_valeur<=self.line_THOP_Rate_slider.cget('to'):
            self.line_THOP_Rate_slider.set(nouvelle_valeur)
    def deplacer_gauche_line_THOP_gamma_slider(self,event):
        #deplacer le curseur line_THOP_gamma_slider vers la gauche
        nouvelle_valeur=self.line_THOP_gamma_slider.get()-1
        if nouvelle_valeur>=self.line_THOP_gamma_slider.cget('from'):
            self.line_THOP_gamma_slider.set(nouvelle_valeur)
    def deplacer_droite_line_THOP_gamma_slider(self,event):
        #deplacer le curseur line_THOP_gamma_slider vers la droite
        nouvelle_valeur=self.line_THOP_gamma_slider.get()+1
        if nouvelle_valeur<=self.line_THOP_gamma_slider.cget('to'):
            self.line_THOP_gamma_slider.set(nouvelle_valeur)
################################################################################
    def donner_focus(self, event):
        #donner le focus au curseur lorsqu'il es cliqué
        event.widget.focus_set()

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.original_image = cv2.imread(self.image_path)
            self.processed_image = self.original_image.copy()
            self.image_max_size()
            self.display_images()

    def upload_BD_fingerprints(self):
        self.DB_directory=filedialog.askdirectory()
    def upload_Test_fingerprints(self):
        self.fingerprint_directory=filedialog.askdirectory()

    def image_max_size(self):
        if self.original_image is not None:
                original_image_width=self.original_image.shape[1]
                original_image_height=self.original_image.shape[0]

                self.line_THR_L_slider.config(to=original_image_width)
                self.line_THR_l_slider.config(to=original_image_height)
 
                self.line_THT_b_slider.config(to=original_image_width)
                self.line_THT_h_slider.config(to=original_image_height)

                gamma_1=min(int((original_image_width+2)/4), int((original_image_height+2)/2))
                self.line_THH_gamma_slider.config(to=gamma_1)

                gamma_2=min(int((original_image_width+1)/3), int((original_image_height+1)/3))
                self.line_THO_gamma_slider.config(to=gamma_2)
                #####################"PARALLÈLE"#################"
                self.line_THRP_L_slider.config(to=original_image_width)
                self.line_THRP_l_slider.config(to=original_image_height)
 
                self.line_THTP_b_slider.config(to=original_image_width)
                self.line_THTP_h_slider.config(to=original_image_height)

                #gamma=min(int((original_image_width+2)/4), int((original_image_height+2)/2))
                self.line_THHP_gamma_slider.config(to=gamma_1)

                #gamma=min(int((original_image_width+1)/3), int((original_image_height+1)/3))
                self.line_THOP_gamma_slider.config(to=gamma_2)
                
    def display_images(self):
        self.display_image(self.original_image, self.original_label)
        self.display_image(self.processed_image, self.processed_label)

    def display_image(self, image, label):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil_resized=image_pil.resize((self.display_width,self.display_height),Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image_pil_resized)
        
        label.configure(image=image_tk)
        label.image = image_tk

    def update_detection(self, _=None):
        if self.original_image is not None:
            if self.selected_method == "THR":
                self.THR_detect_lines()
            elif self.selected_method == "THT":
                self.THT_detect_lines()
            elif self.selected_method == "THH":
                self.THH_detect_lines()
            elif self.selected_method == "THO":
                self.THO_detect_lines()
            elif self.selected_method == "THRP":
                self.THRP_detect_lines()
            elif self.selected_method == "THTP":
                self.THTP_detect_lines()
            elif self.selected_method == "THHP":
                self.THHP_detect_lines()
            elif self.selected_method == "THOP":
                self.THOP_detect_lines()

    def hide_all_sliders(self):
        self.upload_button.pack_forget()
        self.save_button.pack_forget()

        self.line_THR_threshold_label.pack_forget()
        self.line_THR_threshold_slider.pack_forget()
        
        self.line_THR_Rate_label.pack_forget()
        self.line_THR_Rate_slider.pack_forget()

        self.line_THR_L_label.pack_forget()
        self.line_THR_L_slider.pack_forget()

        self.line_THR_l_label.pack_forget()
        self.line_THR_l_slider.pack_forget()
        ######################################
        self.line_THT_threshold_label.pack_forget()
        self.line_THT_threshold_slider.pack_forget()
        
        self.line_THT_Rate_label.pack_forget()
        self.line_THT_Rate_slider.pack_forget()

        self.line_THT_h_label.pack_forget()
        self.line_THT_h_slider.pack_forget()

        self.line_THT_b_label.pack_forget()
        self.line_THT_b_slider.pack_forget()  
        ########################################""
        self.line_THH_threshold_label.pack_forget()
        self.line_THH_threshold_slider.pack_forget()
        
        self.line_THH_Rate_label.pack_forget()
        self.line_THH_Rate_slider.pack_forget()

        self.line_THH_gamma_label.pack_forget()
        self.line_THH_gamma_slider.pack_forget()  

        ########################################""
        self.line_THO_threshold_label.pack_forget()
        self.line_THO_threshold_slider.pack_forget()
        
        self.line_THO_Rate_label.pack_forget()
        self.line_THO_Rate_slider.pack_forget()

        self.line_THO_gamma_label.pack_forget()
        self.line_THO_gamma_slider.pack_forget()  
        ##########################################
        self.upload_BD_button.pack_forget()
        self.upload_fingerprint_button.pack_forget()
        self.process_fingerprint_button.pack_forget()

        ####################PARALLÈLE###################
        self.n_cpu_label.pack_forget()
        self.n_cpu_slider.pack_forget()

        self.line_THRP_threshold_label.pack_forget()
        self.line_THRP_threshold_slider.pack_forget()
        
        self.line_THRP_Rate_label.pack_forget()
        self.line_THRP_Rate_slider.pack_forget()

        self.line_THRP_L_label.pack_forget()
        self.line_THRP_L_slider.pack_forget()

        self.line_THRP_l_label.pack_forget()
        self.line_THRP_l_slider.pack_forget()
        ######################################
        self.line_THTP_threshold_label.pack_forget()
        self.line_THTP_threshold_slider.pack_forget()
        
        self.line_THTP_Rate_label.pack_forget()
        self.line_THTP_Rate_slider.pack_forget()

        self.line_THTP_h_label.pack_forget()
        self.line_THTP_h_slider.pack_forget()

        self.line_THTP_b_label.pack_forget()
        self.line_THTP_b_slider.pack_forget()  
        ########################################""
        self.line_THHP_threshold_label.pack_forget()
        self.line_THHP_threshold_slider.pack_forget()
        
        self.line_THHP_Rate_label.pack_forget()
        self.line_THHP_Rate_slider.pack_forget()

        self.line_THHP_gamma_label.pack_forget()
        self.line_THHP_gamma_slider.pack_forget()  

        ########################################""
        self.line_THOP_threshold_label.pack_forget()
        self.line_THOP_threshold_slider.pack_forget()
        
        self.line_THOP_Rate_label.pack_forget()
        self.line_THOP_Rate_slider.pack_forget()

        self.line_THOP_gamma_label.pack_forget()
        self.line_THOP_gamma_slider.pack_forget() 

    def show_line_buttons(self):
        self.THR_line_method_radio.pack()
        self.THT_line_method_radio.pack()
        self.THH_line_method_radio.pack()
        self.THO_line_method_radio.pack()

        self.THRP_line_method_radio.pack()
        self.THTP_line_method_radio.pack()
        self.THHP_line_method_radio.pack()
        self.THOP_line_method_radio.pack()

    def hide_line_buttons(self):
        self.THR_line_method_radio.pack_forget()
        self.THT_line_method_radio.pack_forget()
        self.THH_line_method_radio.pack_forget()
        self.THO_line_method_radio.pack_forget()

        self.THRP_line_method_radio.pack_forget()
        self.THTP_line_method_radio.pack_forget()
        self.THHP_line_method_radio.pack_forget()
        self.THOP_line_method_radio.pack_forget()

    def show_fingerprint_button(self):
        self.fingerprint_radio.pack()
        self.fingerprintP_radio.pack()

    def hide_fingerprint_button(self):
        self.fingerprint_radio.pack_forget()
        self.fingerprintP_radio.pack_forget()


    def select_main_method(self):
        self.hide_all_sliders()
        main_method_value = self.main_method_var.get()
        if main_method_value == 1:  # Lines Detection
            self.show_line_buttons()
            self.hide_fingerprint_button()
        elif main_method_value == 2:  # Circles Detection
            self.hide_line_buttons()
            self.show_fingerprint_button()


    def select_method(self):
        method_value = self.method_var.get()
        self.hide_all_sliders()
        if method_value == 1:
            self.selected_method = "THR"

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THR_threshold_label.pack()
            self.line_THR_threshold_slider.pack()

            self.line_THR_Rate_label.pack()
            self.line_THR_Rate_slider.pack()

            self.line_THR_L_label.pack()
            self.line_THR_L_slider.pack()

            self.line_THR_l_label.pack()
            self.line_THR_l_slider.pack()
        elif method_value == 2:
            self.selected_method = "THT"

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THT_threshold_label.pack()
            self.line_THT_threshold_slider.pack()

            self.line_THT_Rate_label.pack()
            self.line_THT_Rate_slider.pack()

            self.line_THT_h_label.pack()
            self.line_THT_h_slider.pack()

            self.line_THT_b_label.pack()
            self.line_THT_b_slider.pack()
        elif method_value == 3:
            self.selected_method = "THH"

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THH_threshold_label.pack()
            self.line_THH_threshold_slider.pack()

            self.line_THH_Rate_label.pack()
            self.line_THH_Rate_slider.pack()

            self.line_THH_gamma_label.pack()
            self.line_THH_gamma_slider.pack()
        elif method_value == 4:
            self.selected_method = "THO"

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THO_threshold_label.pack()
            self.line_THO_threshold_slider.pack()

            self.line_THO_Rate_label.pack()
            self.line_THO_Rate_slider.pack()

            self.line_THO_gamma_label.pack()
            self.line_THO_gamma_slider.pack()
        elif method_value == 5:
            self.selected_method = "fingerprint"
            self.upload_BD_button.pack()
            self.upload_fingerprint_button.pack()
            self.process_fingerprint_button.pack()
        elif method_value == 6:
            self.selected_method = "THRP"

            self.n_cpu_label.pack()
            self.n_cpu_slider.pack()

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THRP_threshold_label.pack()
            self.line_THRP_threshold_slider.pack()

            self.line_THRP_Rate_label.pack()
            self.line_THRP_Rate_slider.pack()

            self.line_THRP_L_label.pack()
            self.line_THRP_L_slider.pack()

            self.line_THRP_l_label.pack()
            self.line_THRP_l_slider.pack()
        elif method_value == 7:
            self.selected_method = "THTP"

            self.n_cpu_label.pack()
            self.n_cpu_slider.pack()

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THTP_threshold_label.pack()
            self.line_THTP_threshold_slider.pack()

            self.line_THTP_Rate_label.pack()
            self.line_THTP_Rate_slider.pack()

            self.line_THTP_h_label.pack()
            self.line_THTP_h_slider.pack()

            self.line_THTP_b_label.pack()
            self.line_THTP_b_slider.pack()
        elif method_value == 8:
            self.selected_method = "THHP"

            self.n_cpu_label.pack()
            self.n_cpu_slider.pack()

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THHP_threshold_label.pack()
            self.line_THHP_threshold_slider.pack()

            self.line_THHP_Rate_label.pack()
            self.line_THHP_Rate_slider.pack()

            self.line_THHP_gamma_label.pack()
            self.line_THHP_gamma_slider.pack()
        elif method_value == 9:
            self.selected_method = "THOP"

            self.n_cpu_label.pack()
            self.n_cpu_slider.pack()

            self.upload_button.pack()
            self.save_button.pack()

            self.line_THOP_threshold_label.pack()
            self.line_THOP_threshold_slider.pack()

            self.line_THOP_Rate_label.pack()
            self.line_THOP_Rate_slider.pack()

            self.line_THOP_gamma_label.pack()
            self.line_THOP_gamma_slider.pack()
        elif method_value == 10:
            self.selected_method = "fingerprintP"

            self.n_cpu_label.pack()
            self.n_cpu_slider.pack()

            self.upload_BD_button.pack()
            self.upload_fingerprint_button.pack()
            self.process_fingerprint_button.pack()
#####################################################################""
    def THR_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THR_threshold_slider.get()
        Alpha=self.line_THR_Rate_slider.get()
        Rate=Alpha/100
        L=self.line_THR_L_slider.get()
        l=self.line_THR_l_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLine.Rectangular(edges,l,L,Rate,threshold)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THR')
        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THT_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THT_threshold_slider.get()
        Alpha=self.line_THT_Rate_slider.get()
        Rate=Alpha/100
        h=self.line_THT_h_slider.get()
        b1=self.line_THT_b_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLine.Triangular2(edges,h,b1,Rate,threshold)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THT')
        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THH_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THH_threshold_slider.get()
        Alpha=self.line_THH_Rate_slider.get()
        Rate=Alpha/100
        gamma=self.line_THH_gamma_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLine.Hexagonal(edges,gamma,Rate,threshold)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THH')
        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THO_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THO_threshold_slider.get()
        Alpha=self.line_THO_Rate_slider.get()
        Rate=Alpha/100
        gamma=self.line_THO_gamma_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500,None, 3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLine.Octogonal(edges,gamma,Rate,threshold)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THO')

        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines: 
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()   
#############################################################""
    def THRP_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THRP_threshold_slider.get()
        Alpha=self.line_THRP_Rate_slider.get()
        Rate=Alpha/100
        L=self.line_THRP_L_slider.get()
        l=self.line_THRP_l_slider.get()
        n_cpu=self.n_cpu_slider.get()
        n_cpu=3
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLineParallel.RectangularP(edges,l,L,Rate,threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THRP')
        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THTP_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THTP_threshold_slider.get()
        Alpha=self.line_THTP_Rate_slider.get()
        Rate=Alpha/100
        h=self.line_THTP_h_slider.get()
        b1=self.line_THTP_b_slider.get()
        n_cpu=self.n_cpu_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLineParallel.TriangularP(edges,h,b1,Rate,threshold, n_cpu)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THTP')
        img2 = self.processed_image    
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THHP_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THHP_threshold_slider.get()
        Alpha=self.line_THHP_Rate_slider.get()
        Rate=Alpha/100
        gamma=self.line_THHP_gamma_slider.get()
        n_cpu=self.n_cpu_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500, apertureSize=3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLineParallel.HexagonalP(edges,gamma,Rate,threshold, n_cpu)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THHP')
        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()

    def THOP_detect_lines(self):
        self.processed_image = self.original_image.copy()
        threshold = self.line_THOP_threshold_slider.get()
        Alpha=self.line_THOP_Rate_slider.get()
        Rate=Alpha/100
        gamma=self.line_THOP_gamma_slider.get()
        n_cpu=self.n_cpu_slider.get()
        colors=(0,255,0)
        #gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(self.processed_image, 200, 500,None, 3)
        #lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        t1=time.time()
        _,_,lines = HoughLineParallel.OctogonalP(edges,gamma,Rate,threshold,n_cpu)
        t2=time.time()
        T=t2-t1
        print(len(lines),'droites détectées en', T, 'secondes avec la THOP')

        img2 = self.processed_image     
        img_shape = img2.shape
        Ny = img_shape[0]
        Nx = img_shape[1]
        
        for rho, theta in lines: 
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a*rho
            y0 = b*rho
            pt1 = (int(x0 + 1000 * (-b)), Ny-int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), Ny-int(y0 - 1000 * (a)))
            cv2.line(img2, pt1, pt2, colors, 1, cv2.LINE_AA)
   
        self.display_images()   
###############################################################
    def THG_fingerprint(self):
        if self.selected_method=="fingerprint":
            Test_Path=self.fingerprint_directory
            DataBase_path=self.DB_directory#Database_test
            seuil_long=10
            seuil_larg=10
            seuil_rot=5
            start = time.time()
            _, Bool=Fingerprint.fingerprint(Test_Path,DataBase_path,seuil_long=10,seuil_larg=10,seuil_rot=5)
            #print('resultats=', results)
            end = time.time()
            if Bool==1 :
                self.identification_message_label.config(text=f"Emprint identifiée", fg="lime")
                self.identification_message_label.pack()
            elif Bool==0 :
                self.identification_message_label.config(text=f"Emprint non identifiée", fg="red")
                self.identification_message_label.pack()
            print("Sequentiel:exécution time(en secondes): %f" %float( end - start)) 
        elif self.selected_method=="fingerprintP":
            Test_Path=self.fingerprint_directory
            DataBase_path=self.DB_directory#Database_test
            seuil_long=10
            seuil_larg=10
            seuil_rot=5
            n_cpu=self.n_cpu_slider.get()
            start = time.time()
            _, Bool=Fingerprint.fingerprintP(Test_Path,DataBase_path,seuil_long,seuil_larg,seuil_rot, n_cpu)
            #print('resultats=', results)
            end = time.time()
            if Bool==1 :
                self.identification_message_label.config(text=f"Emprint identifiée", fg="lime")
                self.identification_message_label.pack()
            elif Bool==0 :
                self.identification_message_label.config(text=f"Emprint non identifiée", fg="red")
                self.identification_message_label.pack()
            print("Parallel:exécution time(en secondes): %f" %float( end - start)) 


    def save_image (self):
        if self.processed_image is not None:
            base_name=os.path.basename(self.image_path)
            name, ext=os.path.splitext(base_name)
            if self.selected_method=="THR":
                seuil=self.line_THR_threshold_slider.get()
                alpha=self.line_THR_Rate_slider.get()
                L=self.line_THR_L_slider.get()
                l=self.line_THR_l_slider.get()
                save_path=(f"THR_{name}_seuil{seuil}_alpha{alpha}_L{L}_l{l}{ext}")
            elif self.selected_method=="THT":
                seuil=self.line_THT_threshold_slider.get()
                alpha=self.line_THT_Rate_slider.get()
                b=self.line_THT_b_slider.get()
                h=self.line_THT_h_slider.get()
                save_path=(f"THT_{name}_seuil{seuil}_alpha{alpha}_b{b}_h{h}{ext}")
            elif self.selected_method=="THH":
                seuil=self.line_THH_threshold_slider.get()
                alpha=self.line_THH_Rate_slider.get()
                gamma=self.line_THH_gamma_slider.get()
                save_path=(f"THH_{name}_seuil{seuil}_alpha{alpha}_gamma{gamma}{ext}")
            elif self.selected_method=="THO":
                seuil=self.line_THO_threshold_slider.get()
                alpha=self.line_THO_Rate_slider.get()
                gamma=self.line_THO_gamma_slider.get()
                save_path=(f"THO_{name}_seuil{seuil}_alpha{alpha}_gamma{gamma}{ext}")
            elif self.selected_method=="THRP":
                seuil=self.line_THRP_threshold_slider.get()
                alpha=self.line_THRP_Rate_slider.get()
                L=self.line_THRP_L_slider.get()
                l=self.line_THRP_l_slider.get()
                save_path=(f"THRP_{name}_seuil{seuil}_alpha{alpha}_L{L}_l{l}{ext}")
            elif self.selected_method=="THTP":
                seuil=self.line_THTP_threshold_slider.get()
                alpha=self.line_THTP_Rate_slider.get()
                b=self.line_THTP_b_slider.get()
                h=self.line_THTP_h_slider.get()
                save_path=(f"THTP_{name}_seuil{seuil}_alpha{alpha}_b{b}_h{h}{ext}")
            elif self.selected_method=="THHP":
                seuil=self.line_THHP_threshold_slider.get()
                alpha=self.line_THHP_Rate_slider.get()
                gamma=self.line_THHP_gamma_slider.get()
                save_path=(f"THHP_{name}_seuil{seuil}_alpha{alpha}_gamma{gamma}{ext}")
            elif self.selected_method=="THOP":
                seuil=self.line_THOP_threshold_slider.get()
                alpha=self.line_THOP_Rate_slider.get()
                gamma=self.line_THOP_gamma_slider.get()
                save_path=(f"THOP_{name}_seuil{seuil}_alpha{alpha}_gamma{gamma}{ext}")
            cv2.imwrite(save_path, self.processed_image)
            print(f"image sauvegarder sous {save_path}")

        else:
            print('image non disponible')
                   

if __name__ == "__main__":
    root = Tk()
    app = HoughVGApp(root)
    root.mainloop()
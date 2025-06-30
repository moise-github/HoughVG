# HoughVG :  Hough on Virtual Grids: Hough transform toolbox for straight-lines detection and fingerprints recognition
HoughVG is a Virtual Grid-Based Hough transform toolbox for straight-lines detection and fingerprints recognition. It brings together several innovative variants of the Virtual Grid-Based Hough transform, including the rectangular, triangular, hexagonal and octagonal Hough transforms for straight-line detection, as well as the generalized Hough transform using virtual rectangular grid, specially adapted for fingerprint recognition.
## Requirements 

### Environment
HoughVG only works on Unix operating systems.
### Additional packages
python3, numpy, opencv, tkinter, matplotlib, pymp, scikit, scipy
## Installation
`pip install houghvg`
## Usage
### Straight-lines detection
### Octogonal Hough Transform (OHT)

```
import cv2
import sys
import os
from HoughVG import HoughLine

# === Paramètres ===
Rate = 0.30
gamma = 2
Threshold = 53
EdgesThresholdMax = 500
EdgesThresholdMin = 200
colors = (0, 255, 0)

# === Chemins ===
# Chemin complet vers l’image
image_path = r"C:\Users\win11\OneDrive\Bureau\8.jpeg"

# Dossier de sortie des résultats
output_folder = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(output_folder, exist_ok=True)

# === Chargement de l’image ===
imge_Build = cv2.imread(image_path)
if imge_Build is None:
    print("[ERREUR] Image introuvable ou illisible :", image_path)
    sys.exit(1)
else:
    print("Image chargée avec succès :")

# === Prétraitement (Canny) ===
def ImgPreprocessing(imge, EdgesThresholdMin, EdgesThresholdMax):
    return cv2.Canny(imge, EdgesThresholdMin, EdgesThresholdMax, None, 3)

img = ImgPreprocessing(imge_Build, EdgesThresholdMin, EdgesThresholdMax)

# === Détection Hough Octogonale ===
accum, accum_max, lines = HoughLine.Octogonal(img, gamma, Rate, Threshold)

# === Affichage des résultats ===
img2 = HoughLine.PlotHoughLine(imge_Build, lines, colors)
cv2.imshow("Image affichée", img2)
cv2.waitKey(0)  # attend une touche pour fermer la fenêtre
cv2.destroyAllWindows()

# === Sauvegarde des résultats ===
filename_base = f'THO_Building_R{int(Rate*100)}_T{Threshold}_G{gamma}_C{EdgesThresholdMin}-{EdgesThresholdMax}'

cv2.imwrite(os.path.join(output_folder, filename_base + '_accum.png'), accum)
cv2.imwrite(os.path.join(output_folder, filename_base + '_accum_max.png'), accum_max)
cv2.imwrite(os.path.join(output_folder, filename_base + '_lines.png'), img2)

print("Résultats enregistrés dans :", os.path.abspath(output_folder))
```
### fingerprints recognition
## Using GUI

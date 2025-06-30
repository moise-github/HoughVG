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
#### Octogonal Hough Transform (OHT)

```
import cv2
import sys
import os
from HoughVG import HoughLine

# === Parameters ===
Rate = 0.30
gamma = 2
Threshold = 53
EdgesThresholdMax = 500
EdgesThresholdMin = 200
colors = (0, 255, 0)

# === Paths ===
# Full path to the image
image_path = r"C:\Users\win11\OneDrive\Bureau\8.jpeg"

# Output folder for results
output_folder = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(output_folder, exist_ok=True)

# === Load the image ===
imge_Build = cv2.imread(image_path)
if imge_Build is None:
    print("[ERROR] Image not found or unreadable:", image_path)
    sys.exit(1)
else:
    print("Image loaded successfully:")

# === Preprocessing (Canny) ===
def ImgPreprocessing(imge, EdgesThresholdMin, EdgesThresholdMax):
    return cv2.Canny(imge, EdgesThresholdMin, EdgesThresholdMax, None, 3)

img = ImgPreprocessing(imge_Build, EdgesThresholdMin, EdgesThresholdMax)

# === Application of OHT ===
accum, accum_max, lines = HoughLine.Octogonal(img, gamma, Rate, Threshold)

# === Display  results ===
img2 = HoughLine.PlotHoughLine(imge_Build, lines, colors)
cv2.imshow("Image affichée", img2)
cv2.waitKey(0)  
cv2.destroyAllWindows()

# === Save results ===
filename_base = f'THO{int(Rate*100)}_T{Threshold}_G{gamma}_C{EdgesThresholdMin}-{EdgesThresholdMax}'

cv2.imwrite(os.path.join(output_folder, filename_base + '_accum.png'), accum)
cv2.imwrite(os.path.join(output_folder, filename_base + '_accum_max.png'), accum_max)
cv2.imwrite(os.path.join(output_folder, filename_base + '_lines.png'), img2)

print("Results saved in:", os.path.abspath(output_folder))
```
#### Parallised Octogonal Hough Transform (POHT)
```
import cv2
import sys
import os
from HoughVG import HoughLineParallel

# === Paramètres ===
Rate = 0.30
gamma = 2
Threshold = 53
EdgesThresholdMax = 500
EdgesThresholdMin = 200
colors = (0, 255, 0)
n_cpu = 3

# === Paths ===
# Full path to the image
image_path = ...

# Output folder for results
output_folder = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(output_folder, exist_ok=True)

# === Load the image ===
imge_Build = cv2.imread(image_path)
if imge_Build is None:
    print("[ERROR] Image not found or unreadable:", image_path)
    sys.exit(1)
else:
    print("Image loaded successfully:")

# === Preprocessing (Canny) ===
def ImgPreprocessing(imge, EdgesThresholdMin, EdgesThresholdMax):
    return cv2.Canny(imge, EdgesThresholdMin, EdgesThresholdMax, None, 3)

img = ImgPreprocessing(imge_Build, EdgesThresholdMin, EdgesThresholdMax)

# === Application of POHT ===
accum, accum_max, lines = HoughLineParallel.OctogonalP(img, gamma, Rate, Threshold, n_cpu)

# === Display  results ===
img2 = HoughLineParallel.PlotHoughLineP(imge_Build, lines, colors)
cv2.imshow("Image affichée", img2)
cv2.waitKey(0)  
cv2.destroyAllWindows()

# === Save results ===
filename_base = f'POHT{int(Rate*100)}_T{Threshold}_G{gamma}_C{EdgesThresholdMin}-{EdgesThresholdMax}'

cv2.imwrite(os.path.join(output_folder, filename_base + '_accum.png'), accum)
cv2.imwrite(os.path.join(output_folder, filename_base + '_accum_max.png'), accum_max)
cv2.imwrite(os.path.join(output_folder, filename_base + '_lines.png'), img2)

print("Results saved in :", os.path.abspath(output_folder))
```
### fingerprints recognition
```
# Paths
    test_path = "/home/moses/Bureau/Projet_HoughVG_software_impact_27_12_2024/data/fingerprint"
    database_path = "/home/moses/Bureau/Projet_HoughVG_software_impact_27_12_2024/data/Big_DB"
    
    # Threshold parameters
    length_threshold = 10
    width_threshold = 10
    rotation_threshold = 5
    
    scale = 3
    precision = 0
    
    # Run fingerprint matching
    matched = Fingerprint.fingerprint(
        test_path, 
        database_path, 
        length_threshold, 
        width_threshold, 
        rotation_threshold, 
        scale, 
        precision
    )
    
    # Display result
    if matched:
        print("Fingerprint identified")
    else:
        print("Fingerprint not identified")
```
## Using GUI

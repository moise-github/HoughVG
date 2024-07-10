from setuptools import setup

VERSION = "0.0.1"

setup(
    name="HoughVG",
    author="Moïse OUEDRAOGO",
    author_email="moisewedra@gmail.com",
    version=VERSION,
    #url = 'http://mon_projet.org',
    #license="MIT License",
    #url="https://github.com/classner/pymp",
    #download_url="https://github.com/classner/pymp/tarball/v{0}".format(VERSION),
    packages = {'HoughVG'},
    description = 'Une boîte à outils pour la Transformée de Hough',
    #readme=README.md
    install_requires=['numpy>=1.24.2','opencv-contrib-python>=4.7.0.72','pymp-pypi>=0.5.0','matplotlib>=3.6.3', 'scipy>=1.10.1','scikit-image>=0.21.0'],
    #long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    keywords=["Hough transform", "pymp", "parallelism","mesh","virtual grid","fingerprint"],
    classifiers = [
  # How mature is this project? Common values are
  #   3 - Alpha
  #   4 - Beta
  #   5 - Production/Stable
  "Development Status :: 3 - Beta",

  # Indicate who your project is intended for
  "Intended Audience :: Developers",
  "Topic :: Software Development :: Build Tools",

  # Pick your license as you wish (see also "license" above)
  "License :: OSI Approved :: MIT License",

  # Specify the Python versions you support here.
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.6",
  "Programming Language :: Python :: 3.7",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Environment :: MacOS X",
  "Environment :: Linux",
]
)
from setuptools import setup, find_packages
import re
from pathlib import Path

# Read version from __init__.py
init_file = Path("celer_sight_ai/__init__.py").read_text()
version = re.search(r'__version__ = "(.*?)"', init_file).group(1)

setup(
    name="celer_sight_ai",
    version=version,
    url="https://github.com/BioMarkerImaging/celer_sight_ai",
    author="Manos Chaniotakis",
    author_email="manos.chaniotakis.n@gmail.com",
    description="Scientific image analysis software",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "pillow",
    ],
    license="CC BY-NC 4.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",  # specify minimum Python version
    include_package_data=True,  # to include non-Python files specified in MANIFEST.in
)
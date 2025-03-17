# AlignEM

## macOS (steps 1-5 only need to be done once):
1. Have conda installed and on your PATH. If it is not installed already, I recommend the slimmed down [Miniconda installation](https://www.anaconda.com/docs/getting-started/miniconda/install)
2. [Download](https://github.com/joelyancey/AlignEM/archive/refs/heads/main.zip) .zip archive of AlignEM from GitHub.
3. Double click on the .zip archive file to extract it to AlignEM-main
4. In Terminal, change directories to AlignEM-main/. For example if it is in Downloads:
   
   `cd ~/Downloads/AlignEM-main/`
   
   The AlignEM-main directory contains everything the program needs to run. It can be moved around on your file system for convenient access in the future.
6. In Terminal, run from AlignEM-main/ directory:
   
   `conda env create -y -f macOS.yml`
   
   It may take several minutes to build the pre-configured environment. This only must be done once. 
7. *Start here if preceding steps have already been completed*. In Terminal, run from AlignEM-main/ directory:

   `conda activate align-env  # <- Load the environment pre-configuired for macOS`
   
   `python3 alignem.py        # <- Launch AlignEM`
   
   It may take several minutes for the AlignEM GUI to spool up.

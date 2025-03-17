# AlignEM

## macOS (perform steps 1-6 only once):
1. Install conda if it is not already. I recommend the slimmed down [Miniconda installation](https://www.anaconda.com/docs/getting-started/miniconda/install).
2. [Download](https://github.com/joelyancey/AlignEM/archive/refs/heads/main.zip) .zip archive of AlignEM from GitHub.
3. Double click on the .zip archive file to extract
4. In Terminal, change directories to AlignEM-main/. For example if it is in Downloads:
   
   `cd ~/Downloads/AlignEM-main/`
   
   The AlignEM-main directory contains everything the program needs to run. It can be moved out of Downloads for convenient access in the future.
6. In Terminal, run from AlignEM-main/ directory:
   
   `conda env create -y -f macOS.yml`
   
   It may take several minutes to build the pre-configured environment. This only must be done once. 
7. *Start here if preceding steps have already been completed*. In Terminal, run from AlignEM-main/ directory:

   `conda activate align-env  # <- Activate the pre-configured environment named 'align-env'`
   
   `python3 alignem.py        # <- Launch AlignEM`
   
   It may take several minutes for the AlignEM GUI to spool up.

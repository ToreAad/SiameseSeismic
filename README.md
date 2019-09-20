# Requirements:
Python3 with modules specified in requirements.txt

parcel from https://parceljs.org/ for website

# To run:

1. Download f3 dataset from dataunderground place in data folder. It should be called "F3_entire.segy"

2. Do preprocessing steps:
* run "python3 ./siameseNetwork/create_siamese_model.py"
* run "python3 ./webapi/preprocessStep.py"

3. Run webapp:
* run "python3 ./webapi/webapi.py & parcel ./frontend/index.html"
* Open browser at http://127.0.01:1234

# Issues:
K-nearest neighbour classifer is too slow, each prediction takes n log n time where n is amount of training data and we do this operation m^2 times where m is size of image being classified, this makes doing single prediction basically k^3 log k... 

# Attributions:
The siamese neural network code is adapted from https://github.com/ketil-malde/plankton-siamese. 

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
K-nearest neighbour classifer is conceptually nice for classification of siamese network embedding. They kind of complements each other. Siamese network maps similar features close in space, and KNN labels according to what other labeled features are close to unlabeled point. Unfortunately I found this approach to be way to slow. Now the labeling classifier uses random forest trained on a subset of the data labeled in on the webpage, and it works much faster.

# Attributions:
The siamese neural network code is adapted from https://github.com/ketil-malde/plankton-siamese. 

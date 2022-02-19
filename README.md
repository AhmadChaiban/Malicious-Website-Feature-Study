# Malicious Website Feature Study 

URL for all required datasets to run these notebooks can be found <a href="https://drive.google.com/drive/folders/11gqS36uV3bdLvuxeI4cZ2GlKukoLbuzW?usp=sharing" target="_blank">here<a>.

Authors: Ahmad Chaiban, Dusan Sovilj, Hazem Soliman, Geoff Salmon, Xiaodong Lin

## Project Structure 

There are several notebooks of interest for our study, they are highlighted below, 

* `initial_notebook.ipynb` is where some early investigation was done. 
* `Dataset_notebook.ipynb` contains the initial look at 25 datasets. 
* `Dataset_20_phase_1_tests.ipynb` &  `Dataset_20_phase_2_ML.ipynb`, these notebooks pertain to the analysis and ML done on A.K. Singh's dataset. 
* `dataset_surtur.ipynb` deals with our custom dataset GAWAIN. It continues its creation, performs some rounds of ML on it and saves a final copy of it wich can be found <a href="https://drive.google.com/drive/folders/1Uk03X8vFIIMRaOT9oFUhs7JuSnR6OVd0?usp=sharing" target="_blank">here<a>.
* `ML_table.ipynb` is the final notebook where XGBoost was trained on the different feature types and their combinations. 


As for the folders `addon_features`, `data_construction`, and `img_extract`, these folders contain the scripts that were used to create the datasets and how those features were extracted. Specifically the `data_construction` folder contains the necessary pipeline to generate the final dataset `GAWAIN` from the study. 

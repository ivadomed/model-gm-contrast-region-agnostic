# Automatic Segmentation of Spinal Cord Gray Matter Across Multiple MRI Contrasts and Regions

Repository for contrast and region agnostic spinal cord Gray Matter (GM) segmentation project using nnUnetV2.

This repo contains the code for data preprocessing, training and running inferences mainly based on [Spinal Cord Toolbox](https://spinalcordtoolbox.com/stable/index.html) and [nnUnet](https://github.com/MIC-DKFZ/nnUNet).


![GMseg](https://github.com/user-attachments/assets/f53ca06b-7527-40b9-aacc-e645d7079fdc)


# 1. Main Dependencies

- [![SCT](https://img.shields.io/badge/SCT-6.5-green)](https://github.com/spinalcordtoolbox/spinalcordtoolbox/releases/tag/6.5)

- Python 3.10

# 2. Dataset Summary
   
**Table 01 :**      Data with manual segmentations
| Dataset               | Sequence         |Category         | Region           | In-plane res.    | 
|-------------------------|------------------|----------------|-------------------------|--------------------------|
| [marseille-t2s-template](https://doi.org/10.17605/OSF.IO/YMRGK) | 3T T2star      | HC               | cervical, torax, lumbar | 0.47x0.47               | 
| [gmseg-challenge-2016](http://niftyweb.cs.ucl.ac.uk/program.php?p=CHALLENGE)   | 3T T2star        |HC               | cervical           | 0.6×0.6         | 
| inspired               | 3T T2star         | HC DCM SCI       | cervical             | 0.5×0.5       | 
| lumbar-vanderbilt      | 3T T2star       | HC               | lumbar                 | 0.3×0.3           | 
| sct-testing-large      | 3T T2star        | HC MS DCM   | cervical sup. and inf.  (2 runs)  | 0.5×0.5         | 
| sct-testing-large     | 3T MTon_MTR     | HC MS DCM   | cervical sup. and inf. (2 runs)  | 0.9×0.9       | 
| dcm-brno               | 3T T1w ax        | HC               | cervical                   | 0.35×0.35             | 
| hc-ucsf-psir           | 3T PSIR ax         | HC               | c3                         | 0.8x0.8                 | 
| marseille-7T-T2star    | 7T T2star        |  HC MS ALS        | cervical       | 0.18x0.18  0.22x0.22 | 
| marseille-7T-MP2RAGE     | 7T UNIT1   | HC MS ALS AMS    | cervical sup. and inf.  (2 runs)   | 0.3x0.3       |    
| marseille-7T-MP2RAGE     | 7T T1map       | HC MS ALS AMS    | cervical sup. and inf. (2 runs)    | 0.3x0.3           |  

**Table 02 :**      Data without manual segmentations

# 3. Preprocessing
For all contrasts 
- Reorientation to RPI

# 4. Train GM model
## 4.1 Setting up the environment and installation 
1. 
2. 

## 4.2 Convertion of BIDS data to nnUnetV2 

## 4.3 Training 

## 4.4 Running inference

## 4.5. Compute 2D segmentation metrics



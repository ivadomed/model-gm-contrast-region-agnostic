# Automatic Segmentation of Spinal Cord Gray Matter Across Multiple MRI Contrasts and Regions

Repository for contrast and region agnostic spinal cord Gray Matter (GM) segmentation project using nnUnetV2.

This repo contains the code for data preprocessing, training and running inferences mainly based on [Spinal Cord Toolbox](https://spinalcordtoolbox.com/stable/index.html) and [nnUnet](https://github.com/MIC-DKFZ/nnUNet).

![GMseg_II](https://github.com/user-attachments/assets/e47e745d-4917-4064-9486-9958149e3514)

# 1. Main Dependencies

- [![SCT](https://img.shields.io/badge/SCT-7.0-green)](https://github.com/spinalcordtoolbox/spinalcordtoolbox/releases/tag/7.0)

- Python 3.10

# 2. Dataset Summary

<details>
  <summary> Centers/datasets/sites detail: </summary>
   
**Table 01 :**    Training dataset
| Dataset               | Sequence         |Category         | Region           | In-plane res.    | 
|-------------------------|------------------|----------------|-------------------------|--------------------------|
| [marseille-t2s-template](https://doi.org/10.17605/OSF.IO/YMRGK) | 3T T2starw      | HC               | cervical, torax, lumbar | 0.47x0.47               | 
| [gmseg-challenge-2016](http://niftyweb.cs.ucl.ac.uk/program.php?p=CHALLENGE)   | 3T T2starw        |HC               | cervical           | 0.6×0.6         | 
| inspired               | 3T T2starw         | HC DCM SCI       | cervical             | 0.5×0.5       | 
| lumbar-vanderbilt      | 3T T2starw       | HC               | lumbar                 | 0.3×0.3           | 
| sct-testing-large      | 3T T2starw        | HC MS DCM   | cervical sup. and inf.  (2 runs)  | 0.5×0.5         | 
| sct-testing-large     | 3T MTR     | HC MS DCM   | cervical sup. and inf. (2 runs)  | 0.9×0.9       | 
| dcm-brno               | 3T T1w ax        | HC               | cervical                   | 0.35×0.35             | 
| hc-ucsf-psir           | 3T PSIR ax         | HC               | C3                         | 0.8x0.8                 | 
| marseille-7T-T2star    | 7T T2starw        |  HC MS ALS        | cervical       | 0.18x0.18  0.22x0.22 | 
| marseille-7T-MP2RAGE     | 7T UNIT1   | HC MS ALS AMS    | cervical sup. and inf.  (2 runs)   | 0.3x0.3       |    
| marseille-7T-MP2RAGE     | 7T T1map       | HC MS ALS AMS    | cervical sup. and inf. (2 runs)    | 0.3x0.3           |  
| ms-barcelona-psir      | 3T PSIR ax      | HC MS        | C3                  | 0.78×0.78           | 
| hc-lumbar-zurich      | 3T T2starw       | HC               | lumbar                 | 0.5×0.5           | 
| als-basel-ramira      | 3T rAMIRA       | HC ALS PPS SMA       | cervical and lumbar                 | 0.5×0.5           | 
| umass-ms-ge-pioneer3      | 3T PDw       | HC               | cervical            | 0.37×0.37           | 
| umass-siemens-espree1.5      | 1.5T PDw       | HC               | cervica          | 0.39×0.39           | 
| ms-karolinska-2020      | 3T T2star       | MS               | cervical         | 0.35×0.35           | 
| ms-basel-2020      | 3T T2star       | MS           | cervical          | 0.35×0.35           | 
| levin-stroke      | 3T T2star       | Stroke        | cervical                 | 0.5×0.5           | 
| philadelphia-pediatric   | 3T T2star       | Pediatric       | cervical                 | 0.5×0.5           | 
| vanderbilt-7t-swi      | 7T T2star       | HC MS         | cervical                 | 0.29×0.29      | 
| vanderbilt-7t-swi      | 7T QSM       | HC MS         | cervical                 | 0.29×0.29      | 
| vanderbilt-7t-swi      | 7T SWI       | HC MS         | cervical                 | 0.29×0.29      | 

</details>


# 3. Preprocessing
For all contrasts 
- Reorientation to RPI
- Crop the images around the GM mask, keeping all the information in the axial plane.
- Reslice the images to 0.3x0.3 in the axial plane

# 4. Train GM model
## 4.1 Setting up the environment and installation 
1. Create a conda environment with:
```
conda create -n gm-env python=3.10
```

2. Activate the environment:
```
conda activate gm-env
```
3. Install the required packages:
```
pip install -r codes/requirements.txt
```
## 4.2 Convertion of BIDS data to nnUnetV2 
All datasets must be in a BIDS format, and then converted to an nnUnet format with the following command: 
```
python codes/convert_bids_to_nnUNetV2.py --path-data ~/DATASET_BIDS   --path-out  ~/nnUNet_raw/ --contrast T2star --label-suffix label-GM_seg --dataset-name gm-contrast-agnostic --dataset-number 801 --seed 99 --split 0.8 0.2 
```
## 4.3 Training 
1. Plan and preprocessing

To extract specific dataset properties, such as image size, voxel spacing, intensity information, etc. that will be used by nnUnet to design the U-Net configurations with the ecoder recidual econder plans, use: 
```
nnUNetv2_plan_and_preprocess -d 820 --verify_dataset_integrity
```
2. Train

Since the acquisition in several subjects was of 2D axial images perpendicular to the curvature of the SC and at the end stacked in a 3D matrix, we cannot consider the GM images to be a 3D structure for all subjects. So we are going to develop a 2D model. 

To train a 2D model, with  Residual Encoder Presets L use : 
```
nnUNetv2_train 820 2d 2 --npz 
```


## 4.4 Running inference

1. Using `sct_deepseg` 

```
sct_deepseg graymatter -install
```

```
sct_deepseg graymatter -i IMAGE.nii.gz -o IMAGE_gm_seg.nii.gz 
```

2. For datasets in a nnUnet format:

```
nnUNetv2_predict -d Dataset820_gm-seg  -i ~/imagesTs/ -o ~/test_820 -f  2 -c 2d
```

## 4.5. Compute segmentation metrics
As we are evaluating the GM segmentation in 2D images, it is convenient to evaluate the images independently in each 2D slice, for which we can use Dice Score and Haussdorf Distance metrics using the following script:

```
python codes/calculate_2d_metrics.py -gt sub-01_GT_seg.nii.gz -inf sub-01_inference_seg.nii.gz sub-01_inference_seg2.nii.gz -o sub-01.csv
```

# Acknowledgments

## Open datasets :
1. `marseille-t2s-template` : 
        Callot V., Laines-Medina N., Taso M., & Fradet L. (2022). In Vivo Human Spinal Cord MRI data – From cervical to thoraco-lumbar levels. DOI https://doi.org/10.17605/OSF.IO/YMRGK 
2. `gmseg-challenge-2016` : 
        Prados F. et al. (2017). Spinal cord grey matter segmentation challenge. NeuroImage, 152, 312–329. DOI https://doi.org/10.1016/j.neuroimage.2017.03.010 

## Collaborators :
- Virginie Callot (Center for Magnetic Resonance in Biology and Medicine, CRMBM-CEMEREM, UMR 7339, CNRS, Aix-Marseille University, Marseille, France)
- David Gergely and Gupta Sarvagya (Spinal Cord Injury Center, Balgrist University Hospital, University of Zurich, Zurich, Switzerland)
- Kristin P. O'Grady (Vanderbilt University Institute of Imaging Science, Vanderbilt University Medical Center, Nashville, United States)
- Regina Schlaeger (Department of Neurology, University Hospital Basel and University of Basel, Basel, Switzerland)
- Josef Bednarik, Tomas Horak and Petr Kudlicka (Department of Neurology, University Hospital Brno, Brno, Czechia)
- Nico Papinutto (Department of Neurology, University of California, San Francisco, CA, USA)
- Deborah Pareto, Jaume Sastre-Garriga and Alex Rovira (Section of Neuroradiology and Magnetic Resonance Unit, Department of Radiology, Hospital Universitari Vall d'Hebron, Universitat Autònoma de Barcelona, Barcelona, Spain)
- Claudia Wheeler Kingshott (NMR Research Unit, University Department of Clinical Neurology, Institute of Neurology, University College London, Queen Square, London, United Kingdom)
- Seth Smith (Vanderbilt University Institute of Imaging Science, Vanderbilt University Medical Center, Nashville, TN 37232 USA)
- Charidimos Tsagkas (Translational Neuroradiology Section, National Institutes of Health, Bethesda, USA)
- Cristina Granziera (Neurologic Clinic and Policlinic, University Hospital Basel and University of Basel, Basel, Switzerland)
- Feroze Mohamed (Department of Radiology, Jefferson Integrated Magnetic Resonance Imaging Center, Thomas Jefferson University, Philadelphia, Pennsylvania, USA)
- Mindy Levin (School of Physical and Occupational Therapy, Faculty of Medicine and Health Sciences, McGill University, Montreal, Qc, Canada)
- Tobias Granberg (Department of Clinical Neuroscience, Karolinska Institutet, Stockholm, Sweden)
- Christopher Hemond (Laboratory for Neuroimaging Research, Partners Multiple Sclerosis Center, Ann Romney Center for Neurologic Diseases, Departments of Neurology and Radiology, Brigham and Women's Hospital, Harvard Medical School, Boston, Massachusetts 02115, USA)

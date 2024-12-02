# Automatic Segmentation of Spinal Cord Gray Matter Across Multiple MRI Contrasts and Regions
Repo for train a model contrast and region agnostic for segment the spinal cord gray matter

![GMseg](https://github.com/ivadomed/model-gm-contrast-region-agnostic/assets/77469192/f5625a0d-396d-4276-b55e-f4f198214719)


1. Main Dependencies

SCT 6.3

2. Dataset Summary
   
| Dataset                 | Sequence         | GT      | Category         | Region                     | In-plane res. (mm²)     | N. Subjects | Ax-slices per subject | ~ Total 2D slic |
|-------------------------|------------------|---------|------------------|----------------------------|--------------------------|-------------|------------------------|------------------|
| marseille-7T-T2star    | 7T T2star        | Manual  | HC/MS/ALS        | Cervical                   | 0.18 x 0.18<br>0.22x0.22 | 75          | 10                     | 750              | 
| marseille-7T-T1map     | 7T MP2RAGE       | Manual  | HC/MS/ALS/AMS    | Cervical (2 runs)          | 0.3x0.3                 | 91          | 10                     | 910              | 
| marseille-t2s-template | 3T T2star        | Manual  | HC               | Cervical, thoracic, lumbar | 0.47x0.47               | 25          | 15                     | 375              | 
| inspired               | 3T T2star        | Manual  | HC/DCM/SCI       | Cervical                   | 0.5 × 0.5               | 61          | 12                     | 732              | 
| gmseg-challenge-2016   | 3T T2star        | Manual  | HC               | Cervical                   | 0.6 × 0.6               | 40          | 12                     | 480              | 
| lumbar-vanderbilt      | 3T T2star        | Manual  | HC               | Lumbar                     | 0.3 × 0.3               | 53          | 12                     | 636              | 
| dcm-brno               | 3T T1w ax        | Manual  | HC               | Cervical                   | 0.35 × 0.35             | 65          | 30                     | 1950             | 
| hc-ucsf-psir           | 3T PSIR          | Manual  | HC               | C3                         | 0.8x0.8                 | 110         | 1                      | 110              | 
| sct-testing-large      | 3T T2star        | Manual  | HC, MS           | C1-T12                     | 0.5 × 0.5               | 333         | 10                     | 3750             | 
|                        | 3T MTon_MTR      | Manual  | HC, MS           | C1-L5                      | 0.5 × 0.5               | 42          | 10                     | 420              | 
| exvivo-spinal-cord     | 7T T2star        | Manual  | HC               | C3-L5                      | 0.1 × 0.1               | 1           | 4676                   | 4676             | 
|                        | 7T DTI FA        | Manual  | HC               | C3-L5                      | 0.1 × 0.1               | 1           | 4676                   | 4676             | 
|                        | 9.4T T2w         | Manual  | HC               | C1-T12                     | 0.05 × 0.05             | 1           | 1919                   | 1919             | 
| vanderbilt-7t-swi      | 7T T2star, SWI   | NO GT   | HC, MS           | Cervical                   | 0.3 × 0.3               | 17          | 10                     | 170              | 
| levin-stroke           | 3T T2star        | NO GT   | Stroke           | Cervical                   | 0.5 × 0.5               | 12          | 12                     | 144              | 
| philadelphi-pediatric  | 3T T2star        | NO GT   | Pediatric        | Cervical                   | 0.5 × 0.5               | 24          | 10                     | 240              | 

3. Training 

TODO:
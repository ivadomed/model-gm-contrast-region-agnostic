#!/bin/bash

# Define an array of datasets with their respective parameters
datasets=(
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/marseille-t2s-template/T2star label-GM_seg 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/hc-ucsf-psir/acq-ax_PSIR label-GM_seg 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/gmseg-challenge-2016/T2star label-GM_mean_bin 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/lumbar-vanderbilt/acq-axial_T2star label-GM_seg 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/inspired/acq-cspine_T2star label-GM_seg 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/dcm-brno/T1w gmseg 700 0.8 0.2"
    "/home/GRAMES.POLYMTL.CA/nilaia/data_nvme_nilaia/gm_segmentation/sct-testing-large/T2star gmseg-manual 702 0.0 1.0"
	)

# Base path for output directory
path_out="../../nnUNet_raw/"

# Loop through each dataset and execute the Python script
for dataset in "${datasets[@]}"; do
    IFS=" " read -r path_data contrast label_suffix dataset_number split_train split_val <<< "$dataset"
    python convert_bids_to_nnUNetV2.py \
        --path-data "$path_data" \
        --path-out "$path_out" \
        --contrast "$contrast" \
        --label-suffix "$label_suffix" \
        --dataset-name gm-contrast-agnostic \
        --dataset-number "$dataset_number" \
        --seed 99 \
        --split "$split_train" "$split_val" \
        --copy True
done


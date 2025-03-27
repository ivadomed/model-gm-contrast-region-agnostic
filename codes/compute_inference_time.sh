#!/bin/bash

# Input and output directories
IMAGE_DIR="~/nnUNet_raw/Dataset801_gm-contrast-agnostic/imagesTs/"
LABEL_sct_deepseg="inferences_sct_deepseg/"
LABEL_seg_gm_contrast_agnostic="inferences_seg_gm_contrast_agnostic/"

# Output CSV file
CSV_FILE="inference_results_punk.csv"

# Create output directories if they do not exist
mkdir -p $LABEL_sct_deepseg
mkdir -p $LABEL_seg_gm_contrast_agnostic

# Write the CSV header
echo "subject,dimensions,inference_time_sct_deepseg,inference_time_seg_gm_contrast_agnostic" > $CSV_FILE

# Loop through all images in the directory
for input_file in $(ls $IMAGE_DIR); do
    output_file="${input_file%.*}_seg.nii.gz"
    image_path="$IMAGE_DIR/$input_file"

    # Retrieve the 3D dimensions of the image
    dimensions=$(fslinfo "$image_path" | grep -E 'dim1|dim2|dim3' | awk '{print $2}' | paste -sd "x")

    # Measure inference time for sct_deepseg_gm
    start_time=$(date +%s.%N)
    sct_deepseg_gm -i "$image_path" -o "$LABEL_sct_deepseg/$output_file"
    end_time=$(date +%s.%N)
    inference_time_gm=$(echo "$end_time - $start_time" | bc)

    # Measure inference time for seg_gm_contrast_agnostic
    start_time=$(date +%s.%N)
    sct_deepseg -i "$image_path" -o "$LABEL_seg_gm_contrast_agnostic/$output_file" -task seg_gm_contrast_agnostic
    end_time=$(date +%s.%N)
    inference_time_deepseg=$(echo "$end_time - $start_time" | bc)

    # Save the results in the CSV file
    echo "$input_file,$dimensions,$inference_time_gm,$inference_time_deepseg" >> $CSV_FILE
done
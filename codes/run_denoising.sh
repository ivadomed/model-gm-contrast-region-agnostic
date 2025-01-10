#!/bin/bash

# List of subject identifiers
subjects=(sub-CTS03 sub-CTS04 sub-CTS05 sub-CTS09 sub-CTS10 sub-CTS13 sub-CTS14 sub-CTS15 sub-CTS17 sub-CTS20)

# Base directory for data
BASE_DIR="lumbar-marseille"

# Loop through each subject in the list
for subject in "${subjects[@]}"; do
    # Define file paths
    input_image="$BASE_DIR/$subject/ses-SPpre/anat/${subject}_ses-SPpre_acq-ax_T2w.nii.gz"
    denoised_image="$BASE_DIR/$subject/ses-SPpre/anat/${subject}_ses-SPpre_acq-ax_T2w-den.nii.gz"
    gm_template="$BASE_DIR/reg_$subject/template/PAM50_gm.nii.gz"
    synth_image="$BASE_DIR/$subject/ses-SPpre/anat/${subject}_ses-SPpre_acq-ax_T2w-synth.nii.gz"

    echo "Processing subject: $subject"

    # Check if the input image exists
    if [[ ! -f "$input_image" ]]; then
        echo "Error: Input image not found for $subject: $input_image"
        continue
    fi

    # Step 1: Apply denoising
    echo "Running denoising for $subject..."
    "../btkDenoising" -i "$input_image" -o "$denoised_image" -b 5     # From https://pmc.ncbi.nlm.nih.gov/articles/PMC3508300/
    if [[ $? -ne 0 ]]; then
        echo "Error: Denoising failed for $subject"
        continue
    fi

    # Step 2: Synthesize GM data
    echo "Generating synthetic GM data for $subject..."
    python synth_gm_data.py -i "$denoised_image" -s "$gm_template" -f 0.3 -o "$synth_image"
    if [[ $? -ne 0 ]]; then
        echo "Error: GM data synthesis failed for $subject"
        continue
    fi

    # Step complete
    echo "Processing complete for $subject: Output saved to $synth_image"
    echo "---------------------------------------------"
done

echo "All subjects processed."

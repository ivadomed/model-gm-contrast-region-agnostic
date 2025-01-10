#!/bin/bash

# Directories for input images and segmentations
IMAGE_DIR="Dataset702_synth-seg/imagesTr/"
LABEL_SEG="Dataset702_synth-seg/labelsTr/"

# Directories for output images and segmentations
IMAGE_OUT="Dataset708_synth-seg/imagesTr/"
LABEL_OUT="Dataset708_synth-seg/labelsTr/"

# Create output directories if they do not exist
mkdir -p "$IMAGE_OUT"
mkdir -p "$LABEL_OUT"

# Loop through each image in the input directory
for image in "$IMAGE_DIR"*; do
    file_name=$(basename "$image")  # Extract the file name
    
    # Construct specific input and output file names
    if [[ "$file_name" == *_0000.nii.gz ]]; then
        input_file="$file_name"  # File already has _0000, no modification needed
        output_file="${file_name%_0000.nii.gz}.nii.gz"  # Remove _0000 for the output file
    elif [[ "$file_name" == *.nii.gz ]]; then
        input_file="${file_name%.nii.gz}_0000.nii.gz"  # Add _0000 for the input file
        output_file="${file_name%.nii.gz}_000.nii.gz"  # Add _000 for the output file
    else
        echo "Invalid file: $file_name"
        continue
    fi

    # Verify the existence of the input file
    if [[ ! -f "$IMAGE_DIR/$input_file" ]]; then
        echo "Input file not found: $IMAGE_DIR/$input_file"
        continue
    fi

    # Generate a random number for the ghosting effect
    num_ghosts=$(shuf -i 0-10 -n 1)

    # Run the Python script
    echo "Processing: $input_file and $output_file with num_ghosts=$num_ghosts"
    python add_ghost_synthetic.py "$IMAGE_DIR/$input_file"  "$IMAGE_OUT/$input_file"  --num_ghosts "$num_ghosts"
    
    # Copy the corresponding segmentation file to the output directory
    cp "$LABEL_SEG/$output_file" "$LABEL_OUT/$output_file"
done

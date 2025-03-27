import os
import nibabel as nib
import numpy as np
import csv
import argparse

# Set up argparse to accept command-line arguments
parser = argparse.ArgumentParser(description="Generate a CSV with metadata from NIfTI files.")
parser.add_argument("-i", "--input", required=True, help="Input directory containing GM binary segmentation on RPI orientation (.nii.gz)")
parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
args = parser.parse_args()

# Assign arguments to variables
image_dir = args.input
output_csv = args.output

# Create and write the CSV file
with open(output_csv, mode="w", newline="") as file:
    csv_writer = csv.writer(file)
    # Write headers
    csv_writer.writerow(["image_file", "total_shape_z", "2d_gm_masks", "slice_indices_with_value_1"])

    # Iterate over each .nii.gz file in the directory
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".nii.gz"):
            image_path = os.path.join(image_dir, image_file)
            
            # Load the image
            label = nib.load(image_path)
            data_label = label.get_fdata()
            
            # Get dimensions along the z-axis
            shape_z = data_label.shape[2]
            
            # Identify slice indices where there are values equal to 1
            slice_indices_with_value_1 = []
            for i in range(shape_z):
                if np.any(data_label[:, :, i] == 1):
                    slice_indices_with_value_1.append(i)
            gm_masks = len(slice_indices_with_value_1)
            
            # Write data to the CSV file
            csv_writer.writerow([image_file, shape_z, gm_masks, slice_indices_with_value_1])

print(f"CSV generated: {output_csv}")

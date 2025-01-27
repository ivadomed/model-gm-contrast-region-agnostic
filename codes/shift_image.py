"""
Script to shift an image in a radial way and with a random angulation

Details of flags:

-i  : Input anatomical NIfTI file
-s1 : Input segmentation NIfTI file 1
-s2 : Input segmentation NIfTI file 2
-r  : Radial shift distance range (e.g., 20-30 mm)

Usage:
    python shift_image.py -i anat.nii.gz -s1 anat_gmseg.nii.gz -s2 anat_contrast-agnostic-gm_seg.nii.gz  -r 35-50

Author: Nilser Laines Medina
Date: 2025-01-27

"""

import argparse
import numpy as np
import nibabel as nib
import random
import math
import os

def shift_image(input_file, shift_r_range, seg_file1=None, seg_file2=None):
    try:
        anat_img = nib.load(input_file)
        anat_data = anat_img.get_fdata()
        affine = anat_img.affine
        header = anat_img.header

        pixdim = header.get_zooms()
        
        # Parse radius range and select a random value within the range
        r_min, r_max = map(int, shift_r_range.split('-'))
        shift_r_mm = random.randint(r_min, r_max)
        
        # Generate a random angle (integer from 1 to 360 degrees)
        angle = random.randint(1, 360)
        angle_rad = math.radians(angle)
        
        # Convert radial distance to X and Y components
        shift_x_mm = shift_r_mm * math.cos(angle_rad)
        shift_y_mm = shift_r_mm * math.sin(angle_rad)
        
        shift_x = int(round(shift_x_mm / pixdim[0]))
        shift_y = int(round(shift_y_mm / pixdim[1]))
        
        shifted_anat = np.zeros_like(anat_data)
        x_start = max(0, shift_x)
        x_end = anat_data.shape[1] - max(0, -shift_x)
        y_start = max(0, shift_y)
        y_end = anat_data.shape[0] - max(0, -shift_y)

        shifted_anat[y_start:y_end, x_start:x_end, :] = anat_data[max(0, -shift_y):anat_data.shape[0] - max(0, shift_y),
                                                                 max(0, -shift_x):anat_data.shape[1] - max(0, shift_x),
                                                                 :]
        
        base_name = os.path.splitext(os.path.basename(input_file))[0].replace('.nii', '')
        output_anat_path = f"images/{base_name}_radius-{shift_r_mm}_angle-{angle}_0000.nii.gz"
        os.makedirs(os.path.dirname(output_anat_path), exist_ok=True)
        shifted_img = nib.Nifti1Image(shifted_anat, affine, header)
        nib.save(shifted_img, output_anat_path)
        print(f"Anatomical image saved to {output_anat_path} with radius {shift_r_mm} mm and angle {angle} degrees")
        
        for seg_file, seg_dir in zip([seg_file1, seg_file2], ["labels-s1", "labels-s2"]):
            if seg_file:
                seg_img = nib.load(seg_file)
                seg_data = seg_img.get_fdata()
                
                shifted_seg = np.zeros_like(seg_data)
                shifted_seg[y_start:y_end, x_start:x_end, :] = seg_data[max(0, -shift_y):seg_data.shape[0] - max(0, shift_y),
                                                                        max(0, -shift_x):seg_data.shape[1] - max(0, shift_x),
                                                                        :]
                
                seg_output_file = f"{seg_dir}/{base_name}_radius-{shift_r_mm}_angle-{angle}.nii.gz"
                os.makedirs(os.path.dirname(seg_output_file), exist_ok=True)
                shifted_seg_img = nib.Nifti1Image(shifted_seg, affine, header)
                nib.save(shifted_seg_img, seg_output_file)
                print(f"Segmentation image saved to {seg_output_file} with radius {shift_r_mm} mm and angle {angle} degrees")
        
    except Exception as e:
        print(f"Error processing the images: {e}")

def main():
    parser = argparse.ArgumentParser(description='Shift NIfTI images radially with a random angle.')
    parser.add_argument('-i', '--input', required=True, help='Input anatomical NIfTI file')
    parser.add_argument('-s1', '--segmentation1', required=False, help='Input segmentation NIfTI file 1 (optional)')
    parser.add_argument('-s2', '--segmentation2', required=False, help='Input segmentation NIfTI file 2 (optional)')
    parser.add_argument('-r', '--radius', type=str, required=True, help='Radial shift distance range (e.g., 20-30 mm)')
    
    args = parser.parse_args()
    shift_image(args.input, args.radius, args.segmentation1, args.segmentation2)

if __name__ == '__main__':
    main()

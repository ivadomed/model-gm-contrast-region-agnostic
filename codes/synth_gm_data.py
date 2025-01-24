"""
Script to synthesize images with visible GM after PAM50 registration.

Details of flags:

-i : Path to the input T2w image NIfTI file (e.g., ax-T2w.nii.gz)
-s : Path to the GM soft mask (e.g., template/PAM50_gm.nii.gz)
-f : Factor to multiply the soft mask to synthesize the output (float or int)
-o : Path to the output file (e.g., ax-T2w-synth.nii.gz)

Usage:
    python synth_gm_data.py -i ax-T2w.nii.gz -s template/PAM50_gm.nii.gz -f 2 -o ax-T2w-synth.nii.gz

Author: Nilser Laines Medina
Date: 2024-12-16
"""

import nibabel as nib
import numpy as np
import argparse

def main():
    # Configure the argument parser
    parser = argparse.ArgumentParser(description="Synthesize an image by applying Gaussian noise and enhancing the GM visibility.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input NIfTI file (e.g., anat.nii.gz).")
    parser.add_argument("-s", "--softmask", required=True, help="Path to the GM soft mask NIfTI file (e.g., anat_soft.nii.gz).")
    parser.add_argument("-f", "--factor", type=float, required=True, help="Factor to multiply the soft mask for synthesis (float or int).")
    parser.add_argument("-o", "--output", required=True, help="Path to save the synthesized NIfTI file (e.g., out.nii.gz).")
    args = parser.parse_args()

    # Load the soft mask and input image
    soft_mask_data = nib.load(args.softmask)
    soft_mask = np.array(soft_mask_data.get_fdata())
    soft_mask = np.where(soft_mask >= 0.8, 1, soft_mask)
    
    input_image_data = nib.load(args.input)
    input_image = np.array(input_image_data.get_fdata())

    # Generate Gaussian noise
    gaussian_noise = np.random.normal(loc=1, scale=0.02, size=soft_mask.shape)
    gaussian_noise = np.clip(gaussian_noise, 0, 1)

    # Compute the synthesized image
    soft_mask_with_noise = soft_mask * input_image * gaussian_noise
    synthesized_image = soft_mask_with_noise * args.factor + input_image

    # Save the resulting image
    result_img = nib.Nifti1Image(synthesized_image, input_image_data.affine, input_image_data.header)
    nib.save(result_img, args.output)
    print(f"File saved at: {args.output}")

if __name__ == "__main__":
    main()

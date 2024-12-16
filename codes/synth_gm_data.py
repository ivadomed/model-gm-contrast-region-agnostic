import nibabel as nib
import numpy as np
import argparse

def main():
    # Configure the argument parser
    parser = argparse.ArgumentParser(description="Apply Gaussian noise and modify a medical image.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input NIfTI file (anat.nii.gz).")
    parser.add_argument("-s", "--softmask", required=True, help="Path to the soft mask NIfTI file (anat_soft.nii.gz).")
    parser.add_argument("-o", "--output", required=True, help="Path to save the output NIfTI file (out.nii.gz).")
    args = parser.parse_args()

    # Load input data
    mask_soft_data = nib.load(args.softmask)
    mask_soft = np.array(mask_soft_data.get_fdata())

    anat_gm_data = nib.load(args.input)
    anat_gm = np.array(anat_gm_data.get_fdata())

    # Generate Gaussian noise
    gaussian_noise = np.random.normal(loc=1, scale=0.02, size=mask_soft.shape)
    gaussian_noise = np.clip(gaussian_noise, 0, 1)

    # Compute the new image
    mask_soft_with_noise_anat = mask_soft * anat_gm * gaussian_noise
    anat_new = mask_soft_with_noise_anat + anat_gm

    # Save the result
    result_img = nib.Nifti1Image(anat_new, anat_gm_data.affine, anat_gm_data.header)
    nib.save(result_img, args.output)
    print(f"File saved at: {args.output}")

if __name__ == "__main__":
    main()

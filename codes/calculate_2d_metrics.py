import numpy as np
import nibabel as nib
import pandas as pd
import argparse
import os
from scipy.spatial.distance import directed_hausdorff

def dice_coefficient(A_binary, B_binary):
    """Computes the Dice coefficient between two binary segmentations."""
    A_binary = (A_binary > 0).astype(int)
    B_binary = (B_binary > 0).astype(int)
    
    TP = np.sum(A_binary * B_binary)
    FP = np.sum(A_binary * (1 - B_binary))
    FN = np.sum((1 - A_binary) * B_binary)
    
    if TP + FP + FN == 0:
        return 1.0  # Assign Dice = 1 if there is nothing to segment
    
    return 2 * TP / (2 * TP + FP + FN)

def hausdorff_distance(A_binary, B_binary):
    """Computes the Hausdorff distance between two binary segmentations."""
    if np.any(A_binary) and np.any(B_binary):
        return max(directed_hausdorff(A_binary, B_binary)[0], directed_hausdorff(B_binary, A_binary)[0])
    else:
        return np.nan  # Return NaN if one of the segmentations is empty

def extract_subject_name(filepath):
    """Extracts the subject name from the file name."""
    filename = os.path.basename(filepath)
    subject_name = filename.split('_')[0]  # Assuming subject name is the first part of the filename
    return subject_name

def main(gt_path, inf_paths, output_csv):
    """Main function to compute 2D metrics for multiple segmentations and save results to a CSV file."""
    # Load ground truth image
    gt_img = nib.load(gt_path)
    gt_data = np.array(gt_img.get_fdata())

    subject_name = extract_subject_name(gt_path)

    # Load inferred segmentations
    inf_data_list = [np.array(nib.load(inf_path).get_fdata()) for inf_path in inf_paths]

    # Ensure all segmentations have the same shape
    for inf_data in inf_data_list:
        if gt_data.shape != inf_data.shape:
            raise ValueError("All segmentations must have the same shape.")

    results = []
    
    for i in range(gt_data.shape[2]):  # Iterate over slices
        if np.any(gt_data[:, :, i] > 0):  # Process only slices with segmentation
            result = {
                'subject': subject_name,
                'slice': i,
            }
            
            for j, inf_data in enumerate(inf_data_list):
                dice_score = dice_coefficient(gt_data[:, :, i], inf_data[:, :, i])
                hausdorff_dist = hausdorff_distance(gt_data[:, :, i], inf_data[:, :, i])
                
                result[f'dice_inf{j+1}'] = dice_score
                result[f'hausdorff_inf{j+1}'] = hausdorff_dist
            
            results.append(result)

    # Convert results to DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate 2D Dice and Hausdorff metrics for multiple NIfTI segmentations.")
    parser.add_argument("-gt", "--ground_truth", required=True, help="Path to the ground truth NIfTI file.")
    parser.add_argument("-inf", "--inferences", required=True, nargs='+', help="Paths to the inferred segmentation NIfTI files.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the output CSV file.")
    
    args = parser.parse_args()
    main(args.ground_truth, args.inferences, args.output)

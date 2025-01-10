import argparse
import torchio as tio
from pathlib import Path

def apply_random_ghosting(input_path, output_path, num_ghosts, axes):
    """
    Apply Random Ghosting artifact to a given NIfTI image.

    Parameters:
    - input_path: Path to the input NIfTI file.
    - output_path: Path to save the transformed NIfTI file.
    - num_ghosts: Number of ghost lines to generate in the artifact.
    - axes: Axes where the ghosting artifact will be applied.
    """
    # Load the image
    subject = tio.Subject(image=tio.ScalarImage(input_path))
    
    # Configure the RandomGhosting transformation
    ghosting_transform = tio.RandomGhosting(
        num_ghosts=num_ghosts,  # Number of ghosting lines
        axes=axes,              # Axes along which ghosting occurs
        restore=True,           # Restore the original image's intensity after ghosting
        intensity=1.5,          # Intensity of the ghosting effect
    )
    
    # Apply the transformation to the image
    transformed = ghosting_transform(subject)
    transformed_image = transformed['image']
    
    # Save the transformed image to the specified output path
    transformed_image.save(output_path)
    print(f"Image saved to: {output_path}")

def main():
    """
    Parse command-line arguments and apply the Random Ghosting transformation.
    """
    parser = argparse.ArgumentParser(description="Apply Random Ghosting artifact along the axial plane.")
    parser.add_argument("input", type=str, help="Path to the input NIfTI file.")
    parser.add_argument("output", type=str, help="Path to save the transformed NIfTI file.")
    parser.add_argument("--num_ghosts", type=int, default=3, help="Number of ghosting lines (default: 3).")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # Check if the input file exists
    if not input_path.exists():
        print(f"The input file {input_path} does not exist.")
        return
    
    # Apply ghosting only along the -Y axis (represented by index 1 in TorchIO)
    apply_random_ghosting(input_path, output_path, args.num_ghosts, axes=(1,))

if __name__ == "__main__":
    main()

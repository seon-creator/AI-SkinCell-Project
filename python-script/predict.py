from ultralytics import YOLO
from ultralytics import settings
import os
import cv2

def segment_and_save(test_img, model_path, save_img_dir="result", save_msk_dir="result/segment/mask", conf=0.3):
    """
    Perform segmentation on an image using a YOLOv8 model, save the mask coordinates and visualization image, 
    and return the paths to the saved files.

    Args:
        test_img (str): Path to the input image.
        model_path (str): Path to the trained YOLOv8 model.
        save_img_dir (str): Directory to save images and results.
        save_msk_dir (str): Directory to save mask files.
        conf (float): Confidence threshold for the model.

    Returns:
        tuple: (mask_file_path, result_img_path)
            - mask_file_path (str): Path to the saved mask file (txt).
            - result_img_path (str): Path to the saved segmentation result image (png).
    """

    # Extract the file name (without extension) from test_img
    file_name = os.path.splitext(os.path.basename(test_img))[0]

    # Update settings with the save directory
    settings.update({"runs_dir": save_img_dir})

    # Load a pretrained YOLOv8 model
    model = YOLO(model_path)

    # Run inference on the image
    results = model(test_img, conf=conf)

    # Ensure the save directories exist
    os.makedirs(save_img_dir, exist_ok=True)
    os.makedirs(save_msk_dir, exist_ok=True)

    # Define the paths for saving the output
    mask_file_path = os.path.join(save_msk_dir, f"{file_name}_masks.txt")
    result_img_path = os.path.join(save_img_dir, f"{file_name}_segmented.png")

    # Process the results to save the masks
    for result in results:
        if hasattr(result, 'masks') and result.masks is not None and result.masks.xy:
            masks = result.masks

            # Save mask information to a text file with the image file name
            with open(mask_file_path, 'w') as file:
                for i, xy in enumerate(masks.xyn):  # Using normalized coordinates (xyn)
                    file.write(f"{i} ")
                    for point in xy:
                        file.write(f"{point[0]:.6f} {point[1]:.6f} ")
                    file.write("\n")

            # print(f"Segmentation results saved to {mask_file_path}")

            # Save the segmented image without affecting the original image
            segmented_image = result.plot()  # This method returns the image with segmentation results
            cv2.imwrite(result_img_path, segmented_image)   # Segmented image saved
        else:
            # No masks found in the results
            return None, None

    return mask_file_path, result_img_path
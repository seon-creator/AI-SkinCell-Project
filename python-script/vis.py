import cv2
import numpy as np
import os

def segment_and_analyze(test_img, txt_file_path, result_img_path, pixel_to_real=None, alpha=0.5):
    """
    Perform segmentation visualization on an image, and return the processed image, 
    percentage of area covered by instances, and the number of instances.

    Args:
        test_img (str): Path to the input image.
        txt_file_path (str): Path to the txt file containing segmentation coordinates.
        result_img_path (str): Path where the resulting image will be saved.
        alpha (float): Transparency factor for the overlay (default is 0.5).

    Returns:
        image (numpy.ndarray): Image with segmentation visualization.
        total_area_coverage (float): Percentage of the image covered by the segmented areas.
        instance_count (int): Number of instances detected.
    """

    # Load the image
    image = cv2.imread(test_img)

    # Load segmentation coordinates from the txt file
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

    # Create an overlay image for transparency effect
    overlay = image.copy()
    instance_count = 0
    total_area = 0
    mask_area = 0

    for line in lines:
        data = line.strip().split()
        instance_count += 1
        points = np.array(data[1:], dtype=np.float32).reshape(-1, 2)
        
        # Convert normalized coordinates to absolute coordinates
        h, w = image.shape[:2]
        points[:, 0] *= w
        points[:, 1] *= h

        # Convert points to integer format for OpenCV
        points = points.astype(np.int32)

        # Segmentation 된 영역 계산
        mask_area += cv2.contourArea(points)

        # 탐지된 노화세포 분할정보 이미지에 표시
        cv2.polylines(overlay, [points], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.fillPoly(overlay, [points], color=(0, 0, 255, 128))  # 128 is the alpha channel value

    # Blend the overlay with the original image
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    # 결과 이미지 저장
    cv2.imwrite(result_img_path, image)

    # Calculate the percentage of area covered by instances
    total_area = h * w
    total_area_coverage = (mask_area / total_area) * 100

    # 픽셀 당 실제 길이를 입력하지 않는 경우 비율만 반환
    if pixel_to_real == None:
        return image, total_area_coverage, instance_count
    
    total_area_real = total_area_coverage * pixel_to_real * pixel_to_real
    return image, total_area_coverage, total_area_real, instance_count
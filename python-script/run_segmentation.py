import sys
import os
import json
from predict import segment_and_save
from vis import segment_and_analyze

def main():
    test_img = sys.argv[1]
    model_path = sys.argv[2]
    pixel_to_real = float(sys.argv[3]) if len(sys.argv) > 3 else None
    
    mask_file_path, result_img_path = segment_and_save(test_img, model_path)
    
    if not mask_file_path or not result_img_path:
        result = {
            "mask_file_path": "",
            "result_img_path": "",
            "area_coverage": 0,
            "real_area": 0,
            "instance_count": 0
        }
    else:
        if pixel_to_real:
            image, area_coverage, real_area, instance_count = segment_and_analyze(test_img, mask_file_path, result_img_path, pixel_to_real)
            result = {
                "mask_file_path": mask_file_path,
                "result_img_path": result_img_path,
                "area_coverage": area_coverage,
                "real_area": real_area,
                "instance_count": instance_count
            }
        else:
            image, area_coverage, instance_count = segment_and_analyze(test_img, mask_file_path, result_img_path)
            result = {
                "mask_file_path": mask_file_path,
                "result_img_path": result_img_path,
                "area_coverage": area_coverage,
                "instance_count": instance_count
            }

    json_dir = "result/json"
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, f"{os.path.splitext(os.path.basename(test_img))[0]}_result.json")

    with open(json_path, "w") as f:
        json.dump(result, f)

    # 최종적으로 json_path만 출력
    sys.stdout.write(json_path)

if __name__ == "__main__":
    main()
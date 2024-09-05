import json
import os

# JSON 파일 읽기
with open('instance_seg/dataset/val.json', 'r') as f:
    data = json.load(f)

# 텍스트 파일이 저장될 경로 설정
output_dir = 'instance_seg/dataset/old-cell/labels/val'  # 원하는 경로로 변경
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 각 이미지를 처리
for image in data['images']:
    image_id = image['id']
    file_name = image['file_name']
    width = image['width']
    height = image['height']
    
    # 현재 이미지에 해당하는 annotations 찾기
    annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_id]
    
    # 텍스트 파일에 기록할 내용 생성
    output_path = os.path.join(output_dir, file_name.replace('.png', '.txt'))
    with open(output_path, 'w') as txt_file:
        for annotation in annotations:
            # Segmentation 정보 추출
            segmentation = annotation['segmentation'][0]
            
            # 좌표들을 width와 height로 정규화
            normalized_segmentation = [
                str(round(coord / width, 6)) if i % 2 == 0 else str(round(coord / height, 6)) 
                for i, coord in enumerate(segmentation)
            ]
            
            # 라벨을 "0"으로 시작하고, 그 뒤에 정규화된 좌표들 추가
            line = f"0 {' '.join(normalized_segmentation)}\n"
            
            # 텍스트 파일에 기록
            txt_file.write(line)
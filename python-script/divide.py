# 이미지 가로 1/2 세로 1/2 4등분해서 저장하는 코드
from PIL import Image
import os

def split_image(image_path, output_dir):
    # 이미지 열기
    image = Image.open(image_path)
    image_width, image_height = image.size
    
    # 가로, 세로 2등분
    width_half = image_width // 2
    height_half = image_height // 2
    
    # 4등분된 이미지 저장
    basename = os.path.basename(image_path)
    filename, ext = os.path.splitext(basename)
    
    # 이미지 1: 왼쪽 상단
    img1 = image.crop((0, 0, width_half, height_half))
    img1.save(os.path.join(output_dir, f"{filename}_1{ext}"))
    
    # 이미지 2: 오른쪽 상단
    img2 = image.crop((width_half, 0, image_width, height_half))
    img2.save(os.path.join(output_dir, f"{filename}_2{ext}"))
    
    # 이미지 3: 왼쪽 하단
    img3 = image.crop((0, height_half, width_half, image_height))
    img3.save(os.path.join(output_dir, f"{filename}_3{ext}"))
    
    # 이미지 4: 오른쪽 하단
    img4 = image.crop((width_half, height_half, image_width, image_height))
    img4.save(os.path.join(output_dir, f"{filename}_4{ext}"))

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 폴더 내 모든 파일 처리
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            file_path = os.path.join(input_folder, filename)
            split_image(file_path, output_folder)

# 예시 사용법
input_folder = '/Users/seoseondeok/study/ESG_AI/project/data/processed/old_young/SA-β-gal'
output_folder = '/Users/seoseondeok/study/ESG_AI/project/data/processed/sa-gal-divided'
process_folder(input_folder, output_folder)
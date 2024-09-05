from ultralytics import YOLO

# Load a model
model = YOLO("./model/yolov8-seg.yaml")  # build a new model from YAML
model = YOLO("./model/pretrained/yolov8n-seg.pt")  # load a pretrained model (recommended for training)
model = YOLO("./model/yolov8-seg.yaml").load("./model/pretrained/yolov8n-seg.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="./dataset/old-cell/coco8-seg.yaml", 
                      epochs=100,
                      batch=16,
                      imgsz=640,
                      )

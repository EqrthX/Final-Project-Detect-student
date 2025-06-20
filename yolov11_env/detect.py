from ultralytics import YOLO
import subprocess
import torch
import collections
import cv2
import math
import datetime
def get_center(box):
    x1, y1, x2, y2 = box.xyxy[0]
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return (cx, cy)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] -p2[1])**2)

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    print("ผลลัพธ์ nvidia-smi:n\n", result.stdout)
else:
    print("เกิดข้อผิดพลาด:\n", result.stderr)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# เปิดกล้อง

cap = cv2.VideoCapture(0)

detection_data = collections.defaultdict(lambda: {
    'count' : 0, 
    'detect_person_frame': 0,
    'confidence_person': 0.0, 
    'detect_cellPhone' : 0, 
    'confidence_cellPhone': 0.0,
    'detect_person_cellPhone_frame': 0,
})

start_date = None
end_date = None
hoding_counter = 0
count = 0
msg = ""
frame_counter = 0
max_frame = 60

while cap.isOpened():

    success, frame = cap.read()

    if not success:

        break

    # รัน YOLO แบบ Frame-by-frame

    results = model.predict(source=frame, conf=0.2, device=0, verbose=False)

    # แสดงกรอบตรวจจับลงบนภาพ

    annotated_frame = results[0].plot()

    # แสดงภาพด้วย OpenCV (จะเปิดหน้าต่างแยก)

    cv2.imshow("YOLO Webcam", annotated_frame)
    
    labels_in_frame = set()
    confidences_in_frame = {}

    # แสดง label + confidence ใน console

    for box in results[0].boxes:

        cls = int(box.cls)

        label = model.names[cls]

        conf = box.conf.item()
        
        labels_in_frame.add(label)
        confidences_in_frame[label] = conf
                
        detection_data[label]['count'] += 1
        
        if "person" in labels_in_frame:
            detection_data['person']['detect_person_frame'] += 1
            detection_data[label]['confidence_person'] += conf
        
        if "cell phone" in labels_in_frame:
            detection_data['cell phone']['detect_cellPhone'] += 1
            detection_data['cell phone']['confidence_cellPhone'] += conf
            
        if "person" in labels_in_frame and "cell phone" in labels_in_frame:
            detection_data['person_and_cell_phone']['detect_person_cellPhone_frame'] += 1
            if start_date is None:
                start_date = datetime.datetime.now()
            end_date = datetime.datetime.now()
        else:
            if start_date and end_date:
                duration = (end_date - start_date).seconds
                print(f"⏱️ ถือโทรศัพท์นาน {duration} วินาที")
                start_date = None
                end_date = None
            
        for person_box in box:
            person_center = get_center(person_box)
            for phone_box in box:
                phone_center = get_center(phone_box)
                d = distance(person_center, phone_center)
                if d < 100:
                    msg = "คนถือโทรศัพท์ (ใกล้กัน)"
                    hoding_counter += 1
                else:
                    hoding_counter = 0
                
                if hoding_counter >= 100:
                    msg = "❗ ถือโทรศัพท์ต่อเนื่องเกิน 100 frame"
        # print(f"🔍 {label} ({conf:.2f})")            

    frame_counter += 1
    
    # กด q เพื่อออก

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

cap.release()

cv2.destroyAllWindows()

if frame_counter > 0:
    print("\n Summary after:", frame_counter, "frames:")
    
    person_data = detection_data.get('person')
    cellPhone_data = detection_data.get('cell phone')
    check_person_cellPhone_in_frame = detection_data.get("person_and_cell_phone")
     
    if person_data and person_data['count'] > 0:
        avg_conf = person_data['confidence_person'] / person_data['count']
        print(f"🟢 person: พบ {person_data['count']} ครั้ง, ความแม่นยำเฉลี่ย {avg_conf:.2f}")
    print("-" * 40)
        
    if cellPhone_data and cellPhone_data['count'] > 0:
        avg_conf = cellPhone_data['confidence_cellPhone'] / cellPhone_data['count']
        print(f"🟢 cell phone: พบ {cellPhone_data['count']} ครั้ง, ความแม่นยำเฉลี่ย {avg_conf:.2f}")
    print("-" * 40)
    
    if check_person_cellPhone_in_frame :
        print("มีคนและโทรศัพท์อยู่ด้วยกันทั้งหมด:", check_person_cellPhone_in_frame['detect_person_cellPhone_frame'],'frame')
    
    print(f"{msg}")
    
    if start_date and end_date:
        duration = (end_date - start_date).seconds
        print(f"⏱️ ถือโทรศัพท์นาน {duration} วินาที (จบการตรวจจับ)")
from ai_models import detect_faces

def check_photo_requirements(img):
    requirements = {
        "faces_detected": False,
        "face_centered": False
    }
    
    # Проверка лиц
    faces = detect_faces(img)
    if faces:
        requirements["faces_detected"] = True
        # Проверим, центрировано ли лицо
        width, height = img.size
        center_x, center_y = width // 2, height // 2

        for face in faces:
            # Получаем центр лица
            face_center_x = int(face.xmin * width + (face.width * width) / 2)
            face_center_y = int(face.ymin * height + (face.height * height) / 2)
            
            if abs(face_center_x - center_x) < 50 and abs(face_center_y - center_y) < 50:
                requirements["face_centered"] = True

    return requirements
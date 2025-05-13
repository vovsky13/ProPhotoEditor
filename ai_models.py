import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

def detect_faces(image):
    """Обнаружение лиц на изображении."""
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        # Преобразуем PIL Image в numpy
        img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # Выполняем детекцию лиц
        results = face_detection.process(img_np)
        # Если лица найдены, возвращаем их координаты
        if results.detections:
            return [d.location_data.relative_bounding_box for d in results.detections]
        return []
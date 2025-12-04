from services.face_recognition import find_faces
from services.screen import take_screenshot

def get_idle_faces():
    take_screenshot()
    faces = find_faces()
    return [pt for name, pt in faces.items() if "zzz" in name]

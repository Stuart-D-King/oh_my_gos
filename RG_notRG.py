import os
from sys import argv
import numpy as np
import face_recognition


def ryan_gosling_face():
    img_root = 'data/rg_images'
    face_images = [os.path.join(img_root, f) for f in os.listdir(img_root) if os.path.isfile(os.path.join(img_root, f))]

    faces = [face_recognition.load_image_file(img) for img in face_images]
    face_encodings = [face_recognition.face_encodings(face)[0] for face in faces]
    avg_encoding = sum(face_encodings) / len(face_encodings)

    np.save('data/ryan_gosling_face', avg_encoding)


def compare_faces(new_img):
    ryan_gosling = np.load('ryan_gosling_face.npy')

    unknown_picture = face_recognition.load_image_file(new_img)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    result = face_recognition.compare_faces([ryan_gosling], unknown_face_encoding)

    return result[0]


if __name__ == '__main__':
    # ryan_gosling_face()

    _, img = argv
    compare_faces(img)

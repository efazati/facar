import os
import face_recognition
images_path = '/home/user/projects/facar/image_set/'
known_images_path = images_path + 'known/'
unknown_images_path = images_path + 'unknown/'

def encode_face(im):
    print (im)
    loaded_image = face_recognition.load_image_file(im)
    face_encoding = face_recognition.face_encodings(loaded_image)[0]

    return face_encoding


def load_faces(images):
    result = []
    for im in images:
        result.append(encode_face(im))
 
    return result

def build_db():

    db = []
    for item in os.listdir(known_images_path):
        item_path = os.path.join(known_images_path, item)
        if os.path.isdir(item_path):
            images = {'name': item, 'files': [], 'encoded': []}
            for file in os.listdir(item_path):
                file_path = os.path.join(item_path, file)
                images['files'].append(file_path)
            images['encoded'] = load_faces(images['files'])
            db.append(images)
    return db

def compare(db, path):
    try:
        unknown = encode_face(os.path.join(unknown_images_path, path))
    except:
        return 'Unknowen image'
    names = []
    for item in db:
        results = face_recognition.compare_faces(item['encoded'], unknown)
        if True in results:
            names.append(item['name'])
    return names

def main():
    db = build_db()
    for item in os.listdir(unknown_images_path):
        item_rec_faces = compare(db, item)
        print (item, '->', item_rec_faces)


if __name__ == "__main__": 
    main()
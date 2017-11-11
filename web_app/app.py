import os
import numpy as np
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import face_recognition

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG'])
app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'

RG_message = 'Ryan Gosling!'
not_RG_message = 'NOT Ryan Gosling'

RG_message_multi = 'Ryan Gosling is in the photo!'
not_RG_message_multi = 'Ryan Gosling is NOT in the photo'

# helper function to compare faces
def compare_faces(new_img):
    ryan_gosling = np.load('data/ryan_gosling_face.npy')

    unknown_picture = face_recognition.load_image_file(new_img)
    unknown_face_encodings = face_recognition.face_encodings(unknown_picture)

    results = []
    for face in unknown_face_encodings:
        result = face_recognition.compare_faces([ryan_gosling], face)
        results.append(result[0])

    return results


# helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)

            results = compare_faces('{}'.format(file_path))
            uploaded_img = '../{}'.format(file_path)

            if len(results) > 1:
                if True in results:
                    return render_template('results.html', message=RG_message_multi, uploaded_img=uploaded_img)
                else:
                    return render_template('results.html', message=not_RG_message_multi, uploaded_img=uploaded_img)
            else:
                if results[0] == True:
                    return render_template('results.html', message=RG_message, uploaded_img=uploaded_img)
                else:
                    return render_template('results.html', message=not_RG_message, uploaded_img=uploaded_img)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8105, debug=True)

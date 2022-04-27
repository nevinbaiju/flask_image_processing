from flask import Flask, render_template, request, url_for, flash, redirect
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [ 'jpg', 'png']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'file.png'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/rotate')
    return render_template('index.html')

@app.route('/rotate', methods=['GET', 'POST'])
def rotate():
    if request.method == 'POST':
        img=cv2.imread("static/file.png")

        grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        invert_img=cv2.bitwise_not(grey_img)
        blur_img=cv2.GaussianBlur(invert_img, (111,111),0)
        invblur_img=cv2.bitwise_not(blur_img)
        sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)

        cv2.imwrite('static/file.png', sketch_img)
    return render_template('rotate.html')
app.run(host='0.0.0.0', port=81)

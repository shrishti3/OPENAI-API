from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from image_analysis import analyze_image
from logo_analysis import logoAnalyser
from cta_analysis import ctaAnalyser
from getCoordinates import getCoordinates
app = Flask(__name__)
app.secret_key = API_KEY
# adding path to folder where input image will be save 
app.config['UPLOAD_FOLDER'] = './static/uploads'
# allowing all file types
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# adding route to landing page 
@app.route('/')
def index():
    return render_template('index.html')


# adding route to upload page where post request is made and response in recieved 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # performing image analysis function retrieved from image_analysis.py file
        textResult = analyze_image(filepath)
        logoResult = logoAnalyser(filepath)
        ctaResult = ctaAnalyser(filepath)
        coordinates = getCoordinates(filepath)
        # Display result to a new page showing 
        return render_template('index.html', filename=filename, ctaResult=ctaResult, textResult=textResult, logoResult=logoResult, coordinates=coordinates )
    
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)

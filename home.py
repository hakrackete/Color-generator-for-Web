from flask import Flask, flash, redirect, send_file, url_for, render_template, request
from werkzeug.utils import secure_filename
import os
from ImageToCircle import createCircleImage, createCustomImage
import io
from PIL import ImageColor
from datetime import datetime

app = Flask(__name__)

os.environ["SDL_VIDEODRIVER"] = "dummy" # pythonanywhere Server doesnt want without, would get "no video device" error
Upload_folder = os.getcwd() # Folder where my Images are Uploaded   
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # extensions that i will allow to upload
app.config['UPLOAD_FOLDER'] = Upload_folder

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ["POST", "GET"])
def on_submit():
    if request.method == "POST":
        option = request.form["radioSubmitway"] # this will get the value of the selected Radio-button, i can't use them via names, as they both need the same name
    
        if option == "fileoption":
            file = request.files['file']
            if(file.filename == ''):
                return render_template("error.html")
            filename = secure_filename(file.filename)
            if not(allowed_file(filename)):
                return render_template("error.html")
            UploadLocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(UploadLocation)

            today = datetime.now()
            f = open("WebsiteLOG.txt", "a")
            f.write(str(today) + ' custom Image: "' + filename + '" uploaded with Settings: ')
            f.close()
        else:
            selectedNumber = request.form["numberselector"]
            filename = createCustomImage(selectedNumber)
            UploadLocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            today = datetime.now()
            f = open("WebsiteLOG.txt", "a")
            f.write(str(today) + ' used number "' + str(selectedNumber) + '" with Settings: ')
            f.close()


        # reformats the value of a HTML-form into boolean values
        bw = request.form.get("use_blackwhite") != None
        use_shift = request.form.get("use_shift") != None
        use_light = request.form.get("use_light") != None

        if bw:
            use_grad = request.form.get("use_grad") != None
            first_color = ImageColor.getrgb(request.form["first_colorslider"])
            second_color = ImageColor.getrgb(request.form["second_colorslider"])
            if use_grad:
                gradientshiftrange = int(request.form["gradientshiftslider"]) / 100
            else:
                gradientshiftrange = 0
        else:
            use_grad = False
            gradientshiftrange = 0
            first_color = (0,0,0)
            second_color = (255,255,255)


        background_color = ImageColor.getrgb(request.form["background_colorslider"])

        if use_shift:
            colorswiftrange = int(request.form["shiftslider"])
        else:
            colorswiftrange = 0

        if use_light:
            lightschwiftrange = int(request.form["lightschwiftslider"]) / 100
        else:
            lightschwiftrange = 0    
        
    
            
        iterations = int(request.form["iterationslider"])

        first_radius= int(request.form["min_radius"])
        second_radius= int(request.form["max_radius"])

        min_radius = min(first_radius, second_radius)
        max_radius = max(first_radius, second_radius)

        newFilename = createCircleImage(UploadLocation, colorswiftrange, lightschwiftrange,\
             gradientshiftrange, use_shift, use_light, use_grad, min_radius, max_radius, \
            iterations, bw, filename, first_color, second_color, background_color)

        
        f = open("WebsiteLOG.txt", "a")
        f.write(f"colorswiftrange: {colorswiftrange}, lightschwiftrange: {lightschwiftrange}, gradientshiftrange: {gradientshiftrange}, use_shift: {use_shift}," 
        f" use_grad: {use_grad}, min_radius: {min_radius}, max_radius: {max_radius}, iterations: {iterations}, use_bw: {bw}, first_color {first_color}, second_color {second_color}, background_color{background_color}  \n")
        f.close()

        data = io.BytesIO(open(newFilename, "rb").read())
        os.remove(newFilename)
        
        return send_file(data, newFilename, download_name="Circled " + newFilename)
    else:
        return render_template("menu.html") 

    
if __name__ == "__main__":
    app.run(debug=True)
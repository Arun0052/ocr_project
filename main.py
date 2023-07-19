import os
from flask import *
from flask_cors import CORS
from ocr_script import ocr_main
from ocr_other_info import read_invoice

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# UPLOAD_FOLDER = 'static/upload'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template("index.html")


def pdf_files(file_path,file_name):
    message = {}
    try:
        response = ocr_main(file_path)
        other_response = read_invoice(file_path)
        os.remove(file_path)
        message.update({
            'message': response,
            'other_message': other_response,
            'file_name':file_name
        })
        return message
    except:
        return message

@app.route('/upload', methods=['POST'])
def success():
    message = {
        'status': 404,
        'message': 'user not found'
    }
    try:
        if request.method == 'POST':
            f = request.files['file']
            f.save(f.filename)
            # time.sleep(2)
            response=ocr_main(f.filename)
            other_response= read_invoice(f.filename)
            os.remove(f.filename)
            message.update({
                'status': 200,
                'message': response,
                'other_message':other_response
            })
            return jsonify(message)
            # return render_template("Acknowledgement.html", records=jsonify(message))
    except:
        message = {
            'status': 404,
            'message': 'user not found'
        }
        return jsonify(message)

@app.route('/success', methods=['POST'])
def upload():
    if request.method == "POST":
        response=[]
        files = request.files.getlist("file")
        for file in files:
            file.save(os.path.join(os.getcwd(), file.filename))
            response.append(pdf_files(os.path.join(os.getcwd(), file.filename),file.filename))
    responses={"response":response,'status':200}
    return jsonify(responses)

if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)

from flask import Flask, request, render_template
import os
from threat_intel import get_cve_info

app = Flask(__name__)
app.json.sort_keys = False
UPLOAD_FOLDER = 'data'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_response', methods=['POST'])
def handle_file():
    if 'attachment' not in request.files:
        return 'No file part'

    file = request.files['attachment']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, 'data.csv'))
        user_input = request.form['user_input']
        return get_cve_info(user_input)

if __name__ == "__main__":
    
    app.run(port=8000, debug=True)

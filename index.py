# -*- coding: utf-8 -*- 

import os, sys
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
from flask import render_template
from flask import make_response

import string
import random
from config import Config
from tasks import textextractor

ALLOWED_EXTENSIONS = set(['docx', 'doc', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'hwp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    prefix = ''.join(random.choice(string.ascii_uppercase) for x in range(1))
    return "%s%s"%(prefix,''.join(random.choice(chars) for x in range(size)))

@app.route('/result/<task_id>')
def result(task_id):
    res = textextractor.AsyncResult(task_id)
    if res.ready() == False:
        return jsonify({"status": 1})
    
    c,status = res.get()
    contents = c.decode('utf-8')
    
    return jsonify({"status": status, "contents": contents})
#    return contents

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            workid = id_generator();
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], workid))
            result = textextractor.delay(workid)
            return render_template('result.html',task_id=result.task_id)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

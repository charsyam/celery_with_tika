import os
from celery import Celery
from config import Config

os.environ['CLASSPATH'] = "/home/charsyam/tika-app.jar"
from jnius import autoclass

celery = Celery('tasks', broker=Config.BROKER, backend=Config.BACKEND)

def extract_text(filename):
    Tika = autoclass('org.apache.tika.Tika')
    Metadata = autoclass('org.apache.tika.metadata.Metadata')
    FileInputStream = autoclass('java.io.FileInputStream')

    tika = Tika()
    meta = Metadata()
    contents = tika.parseToString(FileInputStream(filename), meta)
    return contents

@celery.task
def textextractor(workid):
    filename = "%s/%s"%(Config.UPLOAD_FOLDER, workid)
    try:
        contents = extract_text(filename)
        return (contents, 0)
    except:
        return ("tika error", -1)
    finally:
        os.remove(filename)

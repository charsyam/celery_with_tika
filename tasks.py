import os
import shlex
import subprocess
from celery import Celery
from config import Config

celery = Celery('tasks', broker=Config.BROKER, backend=Config.BACKEND)

@celery.task
def textextractor(workid):
    filename = "%s/%s"%(Config.UPLOAD_FOLDER, workid)
    command = "/usr/bin/java -jar %s -t %s > output"%(Config.TIKA_CLASSPATH,filename)

    args = shlex.split(command)
    contents = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    os.remove(filename)
    return (contents, 0)

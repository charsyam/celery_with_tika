import os
from celery import Celery
from config import Config

celery = Celery('tasks', broker=Config.BROKER, backend=Config.BACKEND)

def readfile(filename):
    f = open(filename)
    lines = f.readlines()
    contents = ''.join(lines)
    return contents

@celery.task
def textextractor(workid):
    filename = "%s/%s"%(Config.UPLOAD_FOLDER, workid)
    builds = "%s/%s"%(Config.BUILD_FOLDER, workid)

    command = "mkdir -p %s"%(builds)
    ret = os.system(command)

    os.chdir(builds)

    command = "java -jar ~/tika-app-1.4.jar -t %s > output"%(filename)
    ret = os.system(command)
    if ret != 0:
        return ("tika error", -1)

    contents = readfile("output")
    return (contents, 0)

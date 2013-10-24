import os
import shlex
import subprocess
from celery import Celery
from config import Config

celery = Celery('tasks', broker=Config.BROKER, backend=Config.BACKEND)

def ishwp(filename):
    try:
        command = "hwp5proc cat %s FileHeader"%(filename)
        args = shlex.split(command)
        contents = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        if contents.startswith("HWP Document File"):
            return True
        else:
            return False
    except:
        return False

def readfile(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents

@celery.task
def textextractor(workid):
    filename = "%s/%s"%(Config.UPLOAD_FOLDER, workid)
    builds = "%s/%s"%(Config.BUILD_FOLDER, workid)
    status = 0

    if ishwp(filename) == False:
        command = "/usr/bin/java -jar %s -t %s"%(Config.TIKA_CLASSPATH,filename)

        print command
        args = shlex.split(command)
        try:
            contents = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        except:
            contents = "tika error"
            status = -1
    else:
        try:
            command = "mkdir -p %s"%(builds)
            os.system(command)

            os.chdir(builds)
            command = "hwp5txt %s"%(filename)
            os.system(command)

            txtfile = "%s/%s.txt"%(builds,workid)
            contents = readfile(txtfile)

            command = "rm -rf %s"%(builds)
            os.system(command)
        except:
            contents = "hwp parsing error"
            status = -1

    os.remove(filename)
    return (contents, status)

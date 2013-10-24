import os
import shlex
import subprocess
from celery import Celery
from config import Config

celery = Celery('tasks', broker=Config.BROKER, backend=Config.BACKEND)

def ishwp(filename):
    command = "hwp5proc cat %s FileHeader"%(filename)
    args = shlex.split(command)
    contents = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    if contents.startswith("HWP Document File"):
        return True

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

    if ishwp(filename) == False:
        command = "/usr/bin/java -jar %s -t %s > output"%(Config.TIKA_CLASSPATH,filename)

        args = shlex.split(command)
        contents = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    else:
        command = "mkdir -p %s"%(builds)
        os.system(command)

        os.chdir(builds)
        command = "hwp5txt %s"%(filename)
        os.system(command)

        txtfile = "%s/%s.txt"%(builds,workid)
        contents = readfile(txtfile)

        command = "rm -rf %s"%(builds)
        os.system(command)

    os.remove(filename)
    return (contents, 0)

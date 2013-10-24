class Config(object):
    STATIC_FOLDER='/home/charsyam/celery_with_tika/static'
    UPLOAD_FOLDER='/home/charsyam/celery_with_tika/uploads'
    BUILD_FOLDER='/home/charsyam/celery_with_tika/builds'
    BROKER='redis://localhost:6379/0'
    BACKEND='redis://localhost:6379/0'
    TIKA_CLASSPATH="/home/charsyam/tika-app.jar"

import uuid
import datetime


def upload_image(instance, image):
    today = datetime.datetime.now()
    final_path = '/'.join(['army-gallery', str(instance._meta.model_name), str(uuid.uuid4()) +"."+ str(image.split('.')[-1])])
    return final_path


def upload_file(instance, file):
    today = datetime.datetime.now()
    final_path = '/'.join(['assessor-briefcase', str(instance._meta.model_name), str(uuid.uuid4()) +"."+ str(file.split('.')[-1])])
    return final_path

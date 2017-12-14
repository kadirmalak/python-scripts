import os
import shutil
import tinys3
import re

def backup_folders(access_key_id, secret_access_key, prefix, bucket, course_name):
    conn = tinys3.Connection(access_key_id, secret_access_key,tls=True)
    dirs = (d for d in os.listdir('.') if d.startswith(prefix) and os.path.isdir(d))
    for d in dirs:
        slug = re.sub(r'\W+', '-', d.lower())
        zipname = slug + '.zip'
        
        if not os.path.isfile(zipname): 
            shutil.make_archive(slug, 'zip', d)
            print('created ' + zipname)

        f = open(zipname, 'rb')
        upload_prefix = re.sub(r'\W+', '-', course_name)
        conn.upload(upload_prefix + '-' + zipname, f, bucket)
        print(zipname + ' uploaded')

ACCESS_KEY_ID = '***'
SECRET_ACCESS_KEY = '***'
BUCKET_NAME = '<bucket name>'
FOLDER_PREFIX = '<Week or week generally>'
COURSE_NAME = 'Course Name'

backup_folders(ACCESS_KEY_ID, SECRET_ACCESS_KEY, FOLDER_PREFIX, BUCKET_NAME, COURSE_NAME)

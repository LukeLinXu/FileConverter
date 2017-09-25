import json

import os
import requests
from requests.auth import HTTPBasicAuth

api_key = '5e46cf26a9b2076e2589b7f6118cd57086f50510'


def start_job(source_file, target_format="pdf"):
    endpoint = "https://sandbox.zamzar.com/v1/jobs"
    file_content = {'source_file': open(source_file, 'rb')}
    data_content = {'target_format': target_format}
    res = requests.post(endpoint, data=data_content, files=file_content, auth=HTTPBasicAuth(api_key, ''))
    resp = res.json()
    print(resp)
    job_id = resp["id"]
    check_status(job_id)


def check_status(job_id):
    endpoint = "https://sandbox.zamzar.com/v1/jobs/{}".format(job_id)
    response = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))
    resp = response.json()
    print(resp)
    status = resp["status"]
    print(status)
    if status=='successful':
        file_info = resp["target_files"][0]
        download_file(file_info["name"], file_info["id"])
    else:
        check_status(job_id)


def download_file(local_filename, file_id):
    endpoint = "https://sandbox.zamzar.com/v1/files/{}/content".format(file_id)
    response = requests.get(endpoint, stream=True, auth=HTTPBasicAuth(api_key, ''))
    try:
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

            print("File downloaded")

    except IOError:
        print("Error")


def is_ipa(file):
    return file.endswith("dox") or file.endswith("docx")

if __name__ == '__main__':
    search_dir = os.getcwd()
    files = filter(is_ipa, os.listdir(search_dir))
    for file in files:
        print(file)
        start_job(file)
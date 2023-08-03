import json
import os
from datetime import datetime


def generate_feedback_number():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def save_feedback_to_json(data, folder_path):
    feedback_number = generate_feedback_number()

    feedback_data_file = f"{folder_path}/{feedback_number}/feedback_data.json"

    feedback_data = []
    if os.path.exists(feedback_data_file):
        with open(feedback_data_file, 'r') as f:
            feedback_data = json.load(f)

    feedback_data.append(data)

    with open(feedback_data_file, 'w') as f:
        json.dump(feedback_data, f)


def save_receipt_photo(file, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    feedback_number = generate_feedback_number()
    folder_name = f"{folder_path}/{feedback_number}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = f"{folder_name}/receipt_photo.jpg"
    file.save(filename)
    return filename

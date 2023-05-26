import os
import csv
import datetime
import shutil

main_folder = 'Test_05252023/TOPO.BMP'
output_folder = 'output_images'
csv_file = "MGAI2_date.csv"

image_data = {}

def get_image_creation_time(image_path):
    creation_time = os.path.getmtime(image_path)
    creation_datetime = datetime.datetime.fromtimestamp(creation_time)
    formatted_time = creation_datetime.strftime("%-m/%-d/%Y %-I:%M %p")
    return formatted_time

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        unique_id, study_name, study_id, modified_date, modified_time, visit, eye = row[0].split('\t')
        image_data[modified_date+' '+modified_time] = (unique_id, study_name, study_id, visit, eye)

os.makedirs(output_folder, exist_ok=True)

num_images_saved = 0  # Counter for the number of images saved

for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    if os.path.isdir(subfolder_path):
        image_paths = []
        for image_name in ['upperLid.BMP', 'lowerLid.BMP']:
            image_path = os.path.join(subfolder_path, image_name)
            if not os.path.exists(image_path):
                continue  # Skip to the next iteration if the image file is not found
            image_paths.append(image_path)

        if len(image_paths) == 0:
            continue  # Skip to the next iteration if both 'upperLid.BMP' and 'lowerLid.BMP' are not found

        creation_times = [get_image_creation_time(image_path) for image_path in image_paths]
        unique_id, study_name, study_id, visit, eye = image_data[creation_times[0]]

        for i, creation_time in enumerate(creation_times):
            time = creation_time.replace('/', '_').replace(':', '_')
            image_name = os.path.basename(image_paths[i])
            new_filename = f"{unique_id}_{study_name}_{study_id}_{visit}_{eye}_{time}_{image_name[0].upper()}.BMP"

            output_path = os.path.join(output_folder, new_filename)

            shutil.copy2(image_paths[i], output_path)
            num_images_saved += 1

        print(subfolder_path)
        print(unique_id, study_name, study_id)

print(f"Total images saved: {num_images_saved}")


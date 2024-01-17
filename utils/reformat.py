import os
import glob
import time
import shutil
import cv2
import subprocess
from PIL import Image

def find_image_files(folder_path):
    image_extensions = ['*.jpg', '*.JPG','*.HEIC',  '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, '**', ext), recursive=True))

    return [os.path.abspath(path) for path in image_files]

def get_file_dates(file_path):
    # Get the creation time
    creation_time = os.path.getctime(file_path)
    # Convert it to a human-readable format
    readable_creation_time = time.ctime(creation_time)

    # Get the last modification time
    modification_time = os.path.getmtime(file_path)
    # Convert it to a human-readable format
    readable_modification_time = time.ctime(modification_time)

    # Parse the human-readable modification time
    modification_time_struct = time.strptime(readable_modification_time)
    # Format it as YYYY-MM-DD
    formatted_modification_date = time.strftime("%Y-%m-%d", modification_time_struct)

    return readable_creation_time, formatted_modification_date

def split_path(abs_path):
    directory, file_name = os.path.split(abs_path)
    return directory, file_name

def get_files_dict(folder_path):
    
    
    image_paths = find_image_files(folder_path)
    
    dic_files = {}
    for index, image_path in enumerate(sorted(image_paths)):
        
        date = None
        directory, file_name = split_path(image_path)
        _, file_extension = os.path.splitext(image_path)
        
        if "WIN_" in file_name:
            # Extract the date part from the filename
            # Assuming the filename follows the exact pattern: "WIN_YYYYMMDD_XXXXX.jpg"
            date_part = file_name[4:12]  # Extracts the 'YYYYMMDD' part

            # Reformat to 'YYYY-MM-DD'
            date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
            
        elif "WP_" in file_name:
            # Extract the date part from the filename
            # Assuming the filename follows the exact pattern: "WP_YYYYMMDD_XXXXX.jpg"
            date_part = file_name[3:11]  # Extracts the 'YYYYMMDD' part

            # Reformat to 'YYYY-MM-DD'
            date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
        
        elif "GOPR" in file_name:
            readable_creation_time, formatted_modification_date = get_file_dates(image_path)
            date = formatted_modification_date

        elif "IMG_" in file_name and len(file_name) < 14 and not  "HEIC" in file_name:
            readable_creation_time, formatted_modification_date = get_file_dates(image_path)
            date = formatted_modification_date
        
        elif "IMG_" in file_name and len(file_name) >= 14 and not  "HEIC" in file_name:
            # Extract the date part from the filename
            # Assuming the filename follows the exact pattern: "WIN_YYYYMMDD_XXXXX.jpg"
            date_part = file_name[4:12]  # Extracts the 'YYYYMMDD' part

            # Reformat to 'YYYY-MM-DD'
            date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
        
        else:
            readable_creation_time, formatted_modification_date = get_file_dates(image_path)
            date = formatted_modification_date
            
        if date is not None:
            if date in dic_files.keys():
                date = f"{date}-{index}"
            dic_files[date] = {"directory": directory, "file":file_name, "ext": file_extension}
        
    dic_files = {k: dic_files[k] for k in sorted(dic_files)}

    return dic_files

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder created: {path}")
    else:
        print(f"Folder already exists: {path}")

def delete_folder_if_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Folder deleted: {path}")
    else:
        print(f"Folder does not exist: {path}")

def create_formatted_images(dic_files, export_path):
    
    length = len(dic_files)
    for idx, key in enumerate(dic_files.keys()):
        
        file_ext = dic_files[key]["ext"]
        file_directory = dic_files[key]["directory"]
        file_src_name = dic_files[key]["file"]
        file_dst_name = key
        
        if os.path.exists(os.path.join(export_path, f"{file_dst_name}.jpg")):
            print(f"{file_src_name} already exist in folder")
            continue
        
        if file_ext == ".HEIC":
            convert_heif_to_jpeg(
                heif_path=os.path.join(file_directory, file_src_name), 
                jpeg_path=os.path.join(export_path, f"{file_dst_name}.jpg"))
        else:
            try:
                img = cv2.imread(filename=os.path.join(file_directory, file_src_name))
                cv2.imwrite(filename= os.path.join(export_path, f"{file_dst_name}.jpg"),img=img)
            except Exception as e:
                print(f"An error occurred during image flipping: {e}")
        
        print(f"[{round(100*idx/length, 2)}%] \t {file_src_name} exported as {file_dst_name}")

def convert_heif_to_jpeg(heif_path, jpeg_path):
    try:
        # Convert HEIF to JPEG
        subprocess.run(['heif-convert', heif_path, jpeg_path], check=True)
        print(f"Converted {heif_path} to {jpeg_path}")

        # Flip the JPEG image
        with Image.open(jpeg_path) as img:
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_img.save(jpeg_path)
            print(f"Flipped image saved to {jpeg_path}")

        # Check and delete the auxiliary file if it was created
        aux_file_path = jpeg_path.replace('.jpg', '-urn:com:apple:photo:2020:aux:hdrgainmap.jpg')
        if os.path.exists(aux_file_path):
            os.remove(aux_file_path)
            print(f"Auxiliary file deleted: {aux_file_path}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")
    except Exception as e:
        print(f"An error occurred during image flipping: {e}")

if __name__ == '__main__':
    
    # Replace 'your_folder_path' with the path to the folder you want to search
    folder_path = '/workspace/dev_ws/media/image/'
    export_path = '/workspace/dev_ws/media/export/'
    # delete_folder_if_exists(path=export_path)
    
    dic_files = get_files_dict(folder_path)
    
    # for idx, key in enumerate(dic_files.keys()):
    #     print(idx, key, "\t\t", dic_files[key]["file"], "\t\t",dic_files[key]["directory"], "\t\t",dic_files[key]["ext"])
    # print(f"{len(dic_files)} in dictionary")
    
    # Export images
    create_folder_if_not_exists(path=export_path)
    create_formatted_images(dic_files=dic_files, export_path=export_path)
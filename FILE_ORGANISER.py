import os 
import shutil

folder_name=input("Enter the path Name:").strip()

files={
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Music": [".mp3", ".wav"],
    "Videos": [".mp4", ".mov"],
    "Archives": [".zip", ".rar"],
}


for filename in os.listdir(folder_name):
    file_path=os.path.join(folder_name,filename)
    if os.path.isdir(file_path):
        continue

    _, ex= os.path.splitext(filename)



    moved=False
    for category,extras in files.items():
        if ex.lower() in extras:
            category_folder=os.path.join(folder_name,category)
            os.makedirs(category_folder,exist_ok=True)
            shutil.move(file_path,os.path.join(category_folder,filename))
            print(f"{filename} moved to {category_folder}")
            moved=True
            break

    if not moved:
        other_file=os.path.join(folder_name,"others")
        os.makedirs(other_file,exist_ok=True)
        shutil.move(file_path,os.path.join(other_file,filename))
        print(f"{filename} moved to {other_file}")
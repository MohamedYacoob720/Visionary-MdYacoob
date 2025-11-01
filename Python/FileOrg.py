import os
Source_path = input("Enter the source path: ")
lstfiles = os.scandir(Source_path)
print("Organizing files in the directory...", Source_path)
def arrange_files():
    ext_dict = {
                'Images': ['.jpg', '.png', '.jpeg', '.gif'],
                'Documents': ['.txt', '.pdf', '.docx', '.xlsx'],
                'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac'],
                'Archives': ['.zip', '.rar', '.tar', '.gz'],
                'Executables': ['.exe', '.bat', '.msi']
            }
    filescount_dict = {category: 0 for category in ext_dict.keys()}
    filescount_dict['Others'] = 0
    for file in lstfiles:
        if file.is_dir():
            continue
        else:
            for category, extensions in ext_dict.items():
                if any(file.name.endswith(ext) for ext in extensions):
                    if os.makedirs(os.path.join(Source_path, category), exist_ok=True):
                        dest_dir = os.path.join(Source_path, category)
                        os.rename(file.path, os.path.join(dest_dir, file.name))
                    filescount_dict[category] += 1
                    break
                else:
                    filescount_dict['Others'] += 1
    return filescount_dict        

for ext, filescount in arrange_files().items():
    print(f"Files moved to '{ext}':", filescount)
    
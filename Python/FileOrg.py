import os
Source_path = input("Enter the source path: ")
lstfiles = os.scandir(Source_path)
print("Organizing files in the directory...", Source_path)
for file in lstfiles:
    if file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.jpeg') or file.name.endswith('.gif'):
        if not os.path.exists(os.path.join(Source_path, 'Images')):
            os.makedirs(os.path.join(Source_path, 'Images'))
        os.rename(file.path, os.path.join(Source_path, 'Images', file.name))
    elif file.name.endswith('.txt') or file.name.endswith('.pdf') or file.name.endswith('.docx') or file.name.endswith('.xlsx'):
        if not os.path.exists(os.path.join(Source_path, 'Documents')):
            os.makedirs(os.path.join(Source_path, 'Documents'))
        os.rename(file.path, os.path.join(Source_path, 'Documents', file.name))
    elif file.name.endswith('.mp4') or file.name.endswith('.mkv') or file.name.endswith('.avi') or file.name.endswith('.mov'):
        if not os.path.exists(os.path.join(Source_path, 'Videos')):
            os.makedirs(os.path.join(Source_path, 'Videos'))
        os.rename(file.path, os.path.join(Source_path, 'Videos', file.name))
    elif file.name.endswith('.mp3') or file.name.endswith('.wav') or file.name.endswith('.flac') or file.name.endswith('.aac'):
        if not os.path.exists(os.path.join(Source_path, 'Audio')):
            os.makedirs(os.path.join(Source_path, 'Audio'))
        os.rename(file.path, os.path.join(Source_path, 'Audio', file.name))
    elif file.name.endswith('.zip') or file.name.endswith('.rar') or file.name.endswith('.tar') or file.name.endswith('.gz'):
        if not os.path.exists(os.path.join(Source_path, 'Archives')):
            os.makedirs(os.path.join(Source_path, 'Archives'))
        os.rename(file.path, os.path.join(Source_path, 'Archives', file.name))
    elif file.name.endswith('.exe') or file.name.endswith('.bat') or file.name.endswith('.msi'):
        if not os.path.exists(os.path.join(Source_path, 'Executables')):
            os.makedirs(os.path.join(Source_path, 'Executables'))
        os.rename(file.path, os.path.join(Source_path, 'Executables', file.name))
    else:
        if file.is_dir():
            continue
        if not os.path.exists(os.path.join(Source_path, 'Others')):
            os.makedirs(os.path.join(Source_path, 'Others'))
        os.rename(file.path, os.path.join(Source_path, 'Others', file.name))

folders = ['Images', 'Documents', 'Videos', 'Audio', 'Archives', 'Executables', 'Others']
for dir in folders:  
    if os.path.exists(os.path.join(Source_path, dir)):
        print(f"No.of.files moved to directory '{dir}':", len(os.listdir(os.path.join(Source_path, dir))))
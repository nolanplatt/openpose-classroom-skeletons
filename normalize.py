# normalize.py
# Used to normalize all file names in ./input. Names will be inputImage0.png, inputImage1.png, ..., inputImageN.png.
# This can (and should) be run before running ./process.py. This ensures consistent organization of images, especially in output.

# @author Nolan Platt (nolanplatt.com)
# @date 6/1/2025

import os
import shutil

def normalize_filenames(input_dir="input"):
    print(f"Normalizing filenames in directory: {input_dir}")
    
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')
    
    try:
        filenames = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    image_files = []
    for filename in filenames:
        if filename.lower().endswith(allowed_extensions):
            image_files.append(filename)
    
    image_files.sort() # sorting alphabetically
    
    renamed_count = 0
    for i, old_filename in enumerate(image_files):
        original_base, original_extension = os.path.splitext(old_filename)
        new_filename = f"inputImage{i}{original_extension.lower()}"
        
        old_filepath = os.path.join(input_dir, old_filename)
        new_filepath = os.path.join(input_dir, new_filename)
        
        if old_filename == new_filename:
            print(f"Skipping '{old_filename}', already correctly named.")
            continue
            
        try:
            if os.path.exists(new_filepath):
                print(f"'{new_filename}' already exists. Skipping renaming of '{old_filename}'.")
                continue

            os.rename(old_filepath, new_filepath)
            print(f"Renamed: '{old_filename}' -> '{new_filename}'")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming '{old_filename}' to '{new_filename}': {e}")
            
    if not image_files:
        print("No files found.")
    else:
        print(f"Normalization complete. {renamed_count} files renamed.")

if __name__ == '__main__':
    normalize_filenames() 
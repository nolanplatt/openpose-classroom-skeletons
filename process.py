# process.py
# Processes all images in ./input and outputs skeletonized images and JSON via CMU's OpenPose  to ./output.
# This script will not work unless you have fully and correctly installed OpenPose on your system (by sources).
# You must also configure OpenPose to install Python when you install with CMake - it does not automatically do this.
# If you have questions about the installation process feel free to contact me at nolanplatt@vt.edu.
# Detailed guide on installing can be found on the CMU Perceptual Computing Laboratory site
# https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_installation_0_index.html
# Put all input images in ./input, run ./normalize.py first, then run this script.

# @author Nolan Platt (nolanplatt.com)
# @date 6/1/2025
import sys
import os
import pyopenpose as op
import cv2
import time 

def process_images(input_dir="input", output_dir="output", model_folder="models"):
    # create output directories if they don't exist
    output_images_dir = os.path.join(output_dir, "images")
    output_json_dir = os.path.join(output_dir, "json")
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_json_dir, exist_ok=True)

    # Custom Params (see C:/openpose/include/openpose/flags.hpp)
    # note that I installed openpose in C:/openpose for my machine, but this may differ for you, so make sure to correct the path anywhere that is applicable.
    # I do strongly recommend installing in C:/; if not, make sure you do not install openpose in a directory that contains spaces. This will break it.
    params = dict()
    params["model_folder"] = model_folder # you ma yneed to change this; see above
    params["face"] = True # enable face detection
    params["hand"] = True # enable hand detection
    params["model_pose"] = "BODY_25" # use BODY_25 model 
    params["body"] = 1 # explicitly set for BODY_25
    params["write_json"] = output_json_dir # enable JSON output
    params["net_resolution"] = "656x368"  # Reverted to reduce memory, was -1x736
    params["render_pose"] = 1          # enable CPU rendering 
    params["render_threshold"] = 0.05  # default render threshold
    params["alpha_pose"] = 0.6         # default alpha for pose blending
    params["scale_number"] = 4         # multi-scale processing for better accuracy
    params["scale_gap"] = 0.25          # scale gap
    params["maximize_positives"] = True # 

    # start OP
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # process images
    for image_name_with_ext in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_name_with_ext)
        if not os.path.isfile(image_path):
            continue

        # expecting normalized names like inputImage0.jpg, inputImage1.png, etc.
        # make sure to run ./normalize.py first!
        base_name, original_extension = os.path.splitext(image_name_with_ext)
        
        output_index_str = ""
        if base_name.startswith("inputImage"):
            output_index_str = base_name[len("inputImage"):]
            try:
                int(output_index_str) # ensure integer
            except ValueError:
                print(f"Warning: File '{image_name_with_ext}' seems to follow inputImage pattern but index is not a number. Using original name for output.")
                output_index_str = "" # fallback to original naming or handle differently
        
        if not output_index_str: # non-standard/normalized pattern
            output_image_name = image_name_with_ext
            current_json_files_before = set(f for f in os.listdir(output_json_dir) if f.endswith('.json'))
            can_rename_json = False
            final_json_name = "" # not used if can_rename_json is F
        else:
            output_image_name = f"outputImage{output_index_str}{original_extension}"
            final_json_name = f"outputJSON{output_index_str}.json"
            current_json_files_before = set(f for f in os.listdir(output_json_dir) if f.endswith('.json'))
            can_rename_json = True

        try:
            print(f"Processing {image_name_with_ext}...")
            datum = op.Datum()
            imageToProcess = cv2.imread(image_path)
            if imageToProcess is None:
                print(f"Unknown Error: Could not read image {image_path}. Skipping this image.")
                continue
            
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))

            # output skeletonized image
            output_image_path = os.path.join(output_images_dir, output_image_name)
            cv2.imwrite(output_image_path, datum.cvOutputData)
            print(f"Saved skeletonized image to {output_image_path}")

            # JSON output is handled by OP via params["write_json"]
            # renaming for normalization
            if can_rename_json:
                time.sleep(0.2) # await for file to be written
                
                current_json_files_after = set(f for f in os.listdir(output_json_dir) if f.endswith('.json'))
                new_json_files = current_json_files_after - current_json_files_before

                if len(new_json_files) == 1:
                    openpose_generated_json_filename = new_json_files.pop()
                    openpose_generated_json_path = os.path.join(output_json_dir, openpose_generated_json_filename)
                    final_json_path = os.path.join(output_json_dir, final_json_name)

                    if os.path.exists(final_json_path) and openpose_generated_json_path != final_json_path:
                        print(f"'{final_json_name}' already exists. Overwriting.")
                        os.remove(final_json_path)
                    
                    if openpose_generated_json_path != final_json_path:
                        try:
                            os.rename(openpose_generated_json_path, final_json_path)
                            print(f"Renamed JSON: '{openpose_generated_json_filename}' --> '{final_json_name}'")
                        except Exception as rename_e:
                            print(f"Error renaming JSON file '{openpose_generated_json_filename}' to '{final_json_name}\n': {rename_e}")
                    else: 
                        print(f"Unknown error: Could not determine final state for {openpose_generated_json_filename}")


                elif len(new_json_files) == 0:
                    print(f"No new JSON file detected in '{output_json_dir}' for '{image_name_with_ext}'. Skipping rename.")
            else:
                print(f"JSON output for '{image_name_with_ext}' will use OpenPose default naming (not renamed).")
            

        except Exception as e:
            print(f"Error processing {image_name_with_ext}:\\n {e}")

if __name__ == '__main__':
    try:
        # OP models path
        openpose_models_path = os.environ.get("OPENPOSE_MODELS", "models/") 
        user_specified_path = "C:\\\\openpose\\\\models" # may need to change this! 

        if not (os.path.exists(openpose_models_path) and os.listdir(openpose_models_path)):
            print(f"Default models path '{openpose_models_path}' not found or empty. Trying user-specified path: '{user_specified_path}'")
            if os.path.exists(user_specified_path) and os.listdir(user_specified_path):
                openpose_models_path = user_specified_path
            else:
                print(f"OpenPose models folder not found or empty at {user_specified_path}")
                sys.exit(1)
        
        print(f"Using OpenPose models from: {openpose_models_path}")
        process_images(model_folder=openpose_models_path)
    except Exception as e:
        print(e)
        sys.exit(-1) 
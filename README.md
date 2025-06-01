# openpose-classroom-skeletons

This project iterates through classroom images and creates skeletonizations via OpenPose. It extracts human skeleton keypoints, and saves the results both as images and as JSON keypoints. It also includes `normalize.py` to standardize all input image names for organization, as well as `test.py` to verify your OpenPose Python installation. Installing OpenPose locally can be quite challenging, so if you run into issues installing it as well as the Python library, please reach out to me at <nolanplatt@vt.edu>. 

Relies on [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) from Carnegie Mellon University's Perceptual Computing Laboratory.

## Features

-   Processes all images from `/input`
-   Leverages the OpenPose Python API.
-   Extracts 2D pose keypoints for each detected person.
-   Saves keypoints to corresponding JSON files.
-   Saves images with drawn skeletons, if a person (or persons) were found.
-   Logs all progress to standard out.
-   Includes `test.py` for verifying OpenPose Python setup.
-   Includes `normalize.py` for renaming input images to be more consistent and organized.


## Prerequisites

1.  **OpenPose Installation with Python Bindings:**
    *   You must have OpenPose built from source and installed on your system.
    *   Most importantly, **OpenPose must be compiled with Python support enabled** (`BUILD_PYTHON=ON` in CMake or CMake GUI).
   For detailed OpenPose installation, refer to the [Official OpenPose Installation Documentation](https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_installation_0_index.html) from CMU's Perceptual Computing Laboratory.

2.  **Python Environment:**
    *   Python 3.x
    *   Required Python packages:
        *   `opencv-python`
        *   `numpy`


## Usage

### 1. Testing your OpenPose Installation (`test.py`)

Before running the main processing script, please test your OpenPose Python setup using `test.py`.


### 2. Normalize Images (`normalize.py`)
Place all your input images into `/input`. Then, run `normalize.py` so all files are renamed to be more organized and useful to corrrespond to in `output/json` and `output/images`.

### 3. Processing Images (`process.py`)
Once you verified OpenPose is installed correctly (with Python library) via `test.py`, and you placed all images in `/input` and ran `normalize.py`, you can go ahead and run `process.py`. Please make sure you correct the paths to both your OP install directory and model directory. Personally, my OP is installed locally in `C\openpose`. I would highly recommend installing there. Alternatively, if you place it elsewhere, make sure the path does not contain spaces or whitespaces: this **will** break OpenPose, and thus this script as well.


## Output JSON Format

The `outputJSON{i}.json` file contains the 2D pose keypoints for each detected person in the image. 
{i} represents the number of the image, corresponding to the number in `/input`, which were assigned via `normalize.py`.
The JSON structure is:

```json
{
    "version": 1.3, // OP version
    "people": [
        {
            "person_id":[-1], // id of the person
            "pose_keypoints_2d": [ // keypoints for person #1
                x1, y1, c1,  // Keypoint 0 (e.g., Nose)
                x2, y2, c2,  // Keypoint 1 (e.g., Neck)
                ...
            ]
        },
        {
            "pose_keypoints_2d": [ // keypoints for person #2 (if applicable)
                
            ]
        }
    ]
}
```
Each keypoint triplet `(x, y, c)` represents the x-coordinate, y-coordinate, and confidence score.

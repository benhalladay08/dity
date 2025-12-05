"""
Drive class for naming and managing removable drives

Attributes:
- name (str): User-supplied name of drive
- path (str): Letter identifier of drive
- structure (dict): folder structure of drive.
                    Can either be passed in from a stored dictionary or created upon scanning and initializing a new drive.
- type: (str): Identified type of drive
"""

# todo: Ensure against letter of drive changing for path attr
# todo: Look at using immutable objs (frozenset?) instead of dictionaries
# todo: replace placeholder fileformat with real file location

from dataclasses import dataclass
from pathlib import Path
import json
import os


@dataclass
class Drive:
    name: str
    path: Path
    type: str = None
    structure: dict = None

    def __post_init__(self):
        if self.structure is None:
            self.structure = self.determine_type(self.path)

    def determine_type(self, drivepath: Path) -> dict | None:
        """
        Compare the folder structure of the drive being created with a JSON containing known folder formats
        and identifies matches
        JSON format:
        [
            {
                "type": BRAND1
                "structure": {expected BRAND1 structure as nested dict}
            }
            {
                "type": BRAND2
                "structure": {expected BRAND2 structure as nested dict}
            }
            etc.
        ]
        """
        drive_structure = structure_to_dict(drivepath)
        with open('formatfile.json', 'r') as file:  # see todo
            known_strucs = json.load(file)
        for structure in known_strucs:
            if structure["structure"] == drive_structure:
                self.type = structure["type"]
                return structure
        # if the drive structure is not already in the file, take user input regarding what to do
        # not sure that we wanna be taking user input during the creation of the object
        if input("Structure not found in known formats. Add to known formats? (Y/N) ").lower() == 'y':
            structype = input("What do you want to call this structure type? ")
            known_strucs.append({"type": structype, "structure": drive_structure})
            with open('path/to/jsonformatfile.json', 'w') as file:
                json.dump(known_strucs, file, indent=4)
            return drive_structure
        else:
            pass
            # exit() or something

def structure_to_dict(drivepath: Path) -> dict:
    """Convert a folder structure to a dictionary object for use in python."""
    if len(str(drivepath)) > 5:
        foldername = os.path.basename(drivepath)
    else:
        foldername = str(drivepath)
    struc = {
        "name": foldername,
        "children": []
        }
    for folder in os.listdir(drivepath):
        path = drivepath / folder
        if os.path.isdir(path) and "System Volume Information" not in str(path):
            struc["children"].append(structure_to_dict(path))
    return struc

if __name__ == '__main__':
    pass

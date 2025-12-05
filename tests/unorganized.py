# heehee hoohoo temp testing file
import pytest
import json
from pathlib import Path

# ---- Drive Class Testing ----
import dity.project.classes.drives as drivemod
from dity.project.mapping.drive import DriveMapper

# ungeneralized tests, only work with the specific thumb drive I've been using
def test_create_structure():
    struc = drivemod.structure_to_dict(Path("D:\\"))
    with open('unorganized.json', 'w') as file:
        json.dump(struc, file, indent=2)

def test_create_new_drive():
    drive = drivemod.Drive('mydrive', Path("D:\\"))
    print(drive)


def test_folder_structure():
    compare_drive_struc = {
        "name": 'D:\\',
        "children": [{"name": "folder1",
                      "children": [{"name": "subfolder!",
                                    "children": []
                                    },
                                   {"name": "alsosubfolder",
                                    "children": []
                                    }]
                      },
                     {"name": "folder2",
                      "children": [{"name": "floder",
                                    "children": []
                                    }]
                      },
                     {"name": "folder3",
                      "children": []
                      },
                     {"name": "bforefolder",
                      "children": []
                      }]
    }
    test_drive_struc = drivemod.structure_to_dict(Path('D:/'))
    with open('unorganized.json', 'w') as file:
        json.dump(test_drive_struc, file, indent=4)
    with open('unorganized2.json', 'w') as file:
        json.dump(compare_drive_struc, file, indent=4)
    assert test_drive_struc == compare_drive_struc


def test_from_dict():
    compare_drive = drivemod.Drive('testdrive', Path('D:\\'), 'TEST',
                                   {
                                       "name": "test_folder",
                                       "children": []
                                   },
                                   )
    compare_dict = {
        "name": "testdrive",
        "path": "D:\\",
        "type": "TEST",
        "structure": {
            "name": "test_folder",
            "children": []
        }
    }
    testmapper = DriveMapper()
    test_drive = testmapper.from_dict(compare_dict)


def test_to_dict():
    compare_drive = drivemod.Drive('testdrive', Path('D:\\'), 'TEST',
                                   {
                                       "name": "test_folder",
                                       "children": []
                                   },
                                   )
    compare_dict = {
        "name": "testdrive",
        "path": "D:\\",
        "type": "TEST",
        "structure": {
            "name": "test_folder",
            "children": []
        }
    }
    testmapper = DriveMapper()
    test_dict = testmapper.to_dict(compare_drive)
    assert compare_dict == test_dict
# ----Drive Class Testing End----

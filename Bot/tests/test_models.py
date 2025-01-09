import unittest
from outbreak.models import RootObject  # Assuming the classes are in a file named `model.py`

class TestRootObjectModel(unittest.TestCase):
    def setUp(self):
        self.json_data = {
            "Type": "PresetEntitiesModified",
            "PresetName": "SurvivalManagerPreset",
            "PresetId": "13DC973046AF516A3FE19D8EF0EDFFFB",
            "ModifiedEntities": {
                "ModifiedRCProperties": [
                    {
                        "DisplayName": "Angry Bear Enemy Location",
                        "ID": "24CD500A47334C0BF79CE7B882137FAE",
                        "UnderlyingProperty": {
                            "Name": "RelativeLocation",
                            "DisplayName": "Relative Location",
                            "Description": "Location of the component relative to its parent",
                            "Type": "FVector",
                            "TypePath": "None",
                            "ContainerType": "",
                            "KeyType": "",
                            "Metadata": {
                                "ToolTip": "Location of the component relative to its parent"
                            }
                        },
                        "Metadata": {
                            "Min": "",
                            "Max": ""
                        },
                        "OwnerObjects": [
                            {
                                "Name": "CollisionCylinder",
                                "Class": "CapsuleComponent",
                                "Path": "/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.BorisPlayerCharacter_C_1.CollisionCylinder"
                            }
                        ]
                    }
                ],
                "ModifiedRCFunctions": [],
                "ModifiedRCActors": []
            }
        }

    def test_create_root_object(self):
        # Test if the JSON can be converted into a RootObject instance
        root_object = RootObject.from_dict(self.json_data)
        
        # Validate RootObject attributes
        self.assertEqual(root_object.Type, "PresetEntitiesModified")
        self.assertEqual(root_object.PresetName, "SurvivalManagerPreset")
        self.assertEqual(root_object.PresetId, "13DC973046AF516A3FE19D8EF0EDFFFB")

        # Validate ModifiedEntities and ModifiedRCProperties
        modified_entities = root_object.ModifiedEntities
        self.assertEqual(len(modified_entities.ModifiedRCProperties), 1)

        modified_property = modified_entities.ModifiedRCProperties[0]
        self.assertEqual(modified_property.DisplayName, "Angry Bear Enemy Location")
        self.assertEqual(modified_property.ID, "24CD500A47334C0BF79CE7B882137FAE")
        self.assertEqual(modified_property.UnderlyingProperty.Name, "RelativeLocation")
        self.assertEqual(modified_property.UnderlyingProperty.Metadata.ToolTip, "Location of the component relative to its parent")

        # Validate OwnerObjects
        owner_objects = modified_property.OwnerObjects
        self.assertEqual(len(owner_objects), 1)
        self.assertEqual(owner_objects[0].Name, "CollisionCylinder")
        self.assertEqual(owner_objects[0].Class, "CapsuleComponent")
        self.assertEqual(owner_objects[0].Path, "/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.BorisPlayerCharacter_C_1.CollisionCylinder")


if __name__ == "__main__":
    unittest.main()

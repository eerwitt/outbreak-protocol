import unittest
from outbreak.client import add_uepie_prefix

class TestAddUEPIEPrefix(unittest.TestCase):
    def test_add_uepie_prefix(self):
        # Input object path
        object_path = "/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.BorisPlayerCharacter_C_1.CollisionCylinder"
        
        # Expected output
        expected_path = "/Game/LBG/Maps/UEDPIE_0_L_LBG_Medow.L_LBG_Medow:PersistentLevel.BorisPlayerCharacter_C_1.CollisionCylinder"
        
        # Instance number
        instance_number = 0

        # Call the function
        result = add_uepie_prefix(object_path, instance_number)

        # Assert the result matches the expected output
        self.assertEqual(result, expected_path)

if __name__ == "__main__":
    unittest.main()

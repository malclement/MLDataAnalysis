from unittest import TestCase
from fastapi.testclient import TestClient

from main import app
from backend.tools.custom_enums import FileSize

client = TestClient(app)


class GroundTruthTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_file_size = FileSize.SMALL_2D.name
        cls.invalid_file_size = "INVALID_SIZE"

    def test_get_ground_truth_default(self):
        response = client.get("/gt/")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("node_gt", json_data)
        self.assertIn("gt_to_nodes", json_data)
        self.assertIsInstance(json_data["node_gt"], dict)
        self.assertIsInstance(json_data["gt_to_nodes"], dict)

    def test_get_ground_truth_with_valid_file_size(self):
        response = client.get(f"/gt/?file_size={self.valid_file_size}")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("node_gt", json_data)
        self.assertIn("gt_to_nodes", json_data)

    def test_get_ground_truth_with_invalid_file_size(self):
        response = client.get(f"/gt/?file_size={self.invalid_file_size}")
        self.assertEqual(response.status_code, 422)
        json_data = response.json()
        expected_detail = (
            "value is not a valid enumeration member;"
            " permitted: 'SMALL_2D', 'MEDIUM_2D', 'LARGE_2D'"
        )
        self.assertEqual(json_data["detail"][0]["msg"], expected_detail)
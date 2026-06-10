import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from restaurant_engine.runninghub_cover import (
    extract_output_refs,
    extract_result_url,
    extract_task_status,
)


class TestRunningHubCoverParser(unittest.TestCase):
    def test_runninghub_status_string_data_is_supported(self):
        payload = {"code": 0, "msg": "success", "data": "SUCCESS"}

        self.assertEqual(extract_task_status(payload), "success")

    def test_runninghub_outputs_list_of_strings_is_supported(self):
        payload = {"outputs": ["https://example.com/a.png"]}

        self.assertEqual(extract_output_refs(payload), ["https://example.com/a.png"])
        self.assertEqual(extract_result_url(payload), "https://example.com/a.png")

    def test_runninghub_outputs_list_of_dicts_is_supported(self):
        payload = {"outputs": [{"url": "https://example.com/a.png"}]}

        self.assertEqual(extract_output_refs(payload), ["https://example.com/a.png"])
        self.assertEqual(extract_result_url(payload), "https://example.com/a.png")

    def test_runninghub_outputs_images_dict_is_supported(self):
        payload = {"outputs": {"images": ["https://example.com/a.png"]}}

        self.assertEqual(extract_output_refs(payload), ["https://example.com/a.png"])
        self.assertEqual(extract_result_url(payload), "https://example.com/a.png")

    def test_runninghub_outputs_nested_file_url_is_supported(self):
        payload = {"data": {"outputs": [{"fileUrl": "https://example.com/a.png"}]}}

        self.assertEqual(extract_output_refs(payload), ["https://example.com/a.png"])
        self.assertEqual(extract_result_url(payload), "https://example.com/a.png")

    def test_runninghub_outputs_string_file_ref_is_supported_without_url(self):
        payload = {"data": ["file-id-or-name"]}

        self.assertEqual(extract_output_refs(payload), ["file-id-or-name"])
        self.assertEqual(extract_result_url(payload), "")


if __name__ == "__main__":
    unittest.main()

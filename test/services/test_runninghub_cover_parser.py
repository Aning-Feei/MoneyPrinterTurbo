import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from restaurant_engine.cover_planner import build_high_quality_cover_titles
from restaurant_engine.runninghub_cover import (
    FakeRunningHubCoverClient,
    extract_output_refs,
    extract_result_url,
    extract_task_status,
    generate_runninghub_cover_batch,
)


class TestRunningHubCoverParser(unittest.TestCase):
    def test_cover_title_helper_can_build_six_quality_titles(self):
        titles = build_high_quality_cover_titles(
            "四川火锅，朋友聚餐，热辣氛围，招牌锅底", batch_index=1, count=6
        )

        self.assertEqual(len(titles), 6)
        self.assertEqual(len(set(titles)), 6)
        weak_terms = ("值得一试", "聚餐首选", "发现这家", "必吃", "宝藏", "绝了")
        for title in titles:
            self.assertIsInstance(title, str)
            self.assertTrue(title.strip())
            self.assertFalse(any(term in title for term in weak_terms))

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

    def test_cover_batch_uses_selected_title_for_all_fake_tasks(self):
        client = FakeRunningHubCoverClient()
        selected_images = [
            {"path": f"/tmp/source_{index}.png", "display_name": f"source_{index}.png"}
            for index in range(1, 4)
        ]
        titles = [
            {"title_id": "title_1", "text": "这锅川味越吃越上头", "source": "local_static"},
            {"title_id": "title_2", "text": "朋友聚餐就该吃这锅", "source": "local_static"},
            {"title_id": "title_3", "text": "藏不住的热辣火锅局", "source": "local_static"},
        ]

        with tempfile.TemporaryDirectory() as output_dir:
            report = generate_runninghub_cover_batch(
                theme_text="四川火锅",
                titles=titles,
                selected_images=selected_images,
                output_dir=output_dir,
                batch_index=3,
                aspect_ratio="9:16",
                selected_video_title_id="title_2",
                selected_video_title_text="朋友聚餐就该吃这锅",
                uploaded_image_count=6,
                client=client,
            )

        self.assertEqual(len(client.submitted_tasks), 3)
        self.assertEqual(report["selected_video_title_id"], "title_2")
        self.assertEqual(report["selected_video_title_text"], "朋友聚餐就该吃这锅")
        self.assertEqual(report["uploaded_image_count"], 6)
        self.assertEqual(len(report["variants"]), 3)
        for task in client.submitted_tasks:
            self.assertEqual(task["title_text"], "朋友聚餐就该吃这锅")
            self.assertIn("朋友聚餐就该吃这锅", task["cover_prompt"])
            self.assertIn("比例：9:16", task["cover_prompt"])
            self.assertEqual(task["aspect_ratio"], "9:16")
        for variant in report["variants"]:
            self.assertEqual(variant["title_text"], "朋友聚餐就该吃这锅")
            self.assertIn("朋友聚餐就该吃这锅", variant["cover_prompt"])
            self.assertEqual(variant["aspect_ratio"], "9:16")
            self.assertEqual(variant["external_api_called"], True)


if __name__ == "__main__":
    unittest.main()

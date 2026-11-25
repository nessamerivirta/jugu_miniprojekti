import unittest
from types import SimpleNamespace
from unittest.mock import patch

import app as app_module


class TestEditReference(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()
        self.reference = SimpleNamespace(
            id=5,
            type="book",
            citation_key="existing-key",
            author="Existing Author",
            title="Existing Title",
            publishing_year=2020,
            publisher="Existing Publisher",
        )

    def test_edit_page_displays_current_reference(self):
        with patch("app.get_reference", return_value=self.reference):
            response = self.client.get("/edit_reference/5")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="existing-key"', response.data)
        self.assertIn(b'value="Existing Author"', response.data)
        self.assertIn(b'value="Existing Title"', response.data)
        self.assertIn(b'value="Existing Publisher"', response.data)

    def test_submitting_edit_updates_reference(self):
        with (
            patch("app.get_reference", return_value=self.reference),
            patch("app.update_reference", return_value=True) as update_reference,
        ):
            response = self.client.post(
                "/edit_reference/5",
                data={
                    "type": "book",
                    "citation_key": "updated-key",
                    "author": "Updated Author",
                    "title": "Updated Title",
                    "publishing_year": "2024",
                    "publisher": "Updated Publisher",
                },
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/view_references")
        update_reference.assert_called_once_with(
            5,
            {
                "type": "book",
                "citation_key": "updated-key",
                "author": "Updated Author",
                "title": "Updated Title",
                "publishing_year": 2024,
            },
            "Updated Publisher",
        )


if __name__ == "__main__":
    unittest.main()

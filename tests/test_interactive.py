from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from src import interactive


class InteractiveStartupTests(unittest.TestCase):
    @patch("src.interactive.ClinicalShell")
    def test_main_starts_with_openai_key_only(self, shell_class) -> None:
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"}, clear=True):
            interactive.main()

        shell_class.assert_called_once_with()
        shell_class.return_value.run.assert_called_once_with()

    @patch("src.interactive.ClinicalShell")
    def test_main_starts_without_cloud_keys_for_local_models(self, shell_class) -> None:
        with patch.dict(os.environ, {}, clear=True):
            interactive.main()

        shell_class.assert_called_once_with()
        shell_class.return_value.run.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

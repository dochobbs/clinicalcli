from __future__ import annotations

import io
import os
import sys
import types
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from src.model_manager import ModelManager


class ModelManagerOpenAITests(unittest.TestCase):
    def test_set_model_selects_openai_with_key(self) -> None:
        manager = ModelManager()

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"}, clear=True):
            selected = manager.set_model("gpt-5.1")

        self.assertTrue(selected)
        self.assertEqual(manager.model_type, "openai")
        self.assertEqual(manager.current_model, "gpt-5.1")

    def test_set_model_rejects_openai_without_key_without_mutating_state(self) -> None:
        manager = ModelManager()
        original_state = (manager.model_type, manager.current_model)

        with patch.dict(os.environ, {}, clear=True):
            selected = manager.set_model("gpt-5.1")

        self.assertFalse(selected)
        self.assertEqual((manager.model_type, manager.current_model), original_state)

    def test_call_model_routes_to_openai(self) -> None:
        manager = ModelManager()
        manager.model_type = "openai"
        manager.current_model = "gpt-5.1"

        with patch.object(manager, "_call_openai", return_value="answer") as call_openai:
            result = manager.call_model("system", "question", max_tokens=321)

        self.assertEqual(result, "answer")
        call_openai.assert_called_once_with("system", "question", 321)

    def test_openai_stream_request_and_aggregation(self) -> None:
        request: dict[str, object] = {}

        class FakeCompletions:
            def create(self, **kwargs):
                request.update(kwargs)
                return [
                    SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="Hel"))]),
                    SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=None))]),
                    SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="lo"))]),
                ]

        fake_client = SimpleNamespace(
            chat=SimpleNamespace(completions=FakeCompletions()),
        )
        fake_openai = types.ModuleType("openai")
        fake_openai.OpenAI = lambda **kwargs: self._capture_client(kwargs, fake_client, request)

        manager = ModelManager()
        manager.model_type = "openai"
        manager.current_model = "gpt-5.1"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"}, clear=True):
            with patch.dict(sys.modules, {"openai": fake_openai}):
                with redirect_stdout(io.StringIO()) as output:
                    result = manager._call_openai("system", "question", 456)

        self.assertEqual(result, "Hello")
        self.assertEqual(output.getvalue(), "Hello\n")
        self.assertEqual(request["api_key"], "test-openai-key")
        self.assertEqual(request["model"], "gpt-5.1")
        self.assertEqual(request["max_completion_tokens"], 456)
        self.assertEqual(
            request["messages"],
            [
                {"role": "system", "content": "system"},
                {"role": "user", "content": "question"},
            ],
        )
        self.assertIs(request["stream"], True)

    @staticmethod
    def _capture_client(kwargs, client, request):
        request.update(kwargs)
        return client


if __name__ == "__main__":
    unittest.main()

# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import mock

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import DummyCompleter, Completer
from prompt_toolkit.layout import Window
from prompt_toolkit.widgets import SearchToolbar

from awscli.autoprompt.factory import (
    PromptToolkitKeyBindings, PromptToolkitFactory, CLIPromptBuffer
)
from awscli.autoprompt.history import HistoryCompleter
from awscli.testutils import unittest


class TestPromptToolkitFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PromptToolkitFactory(completer=DummyCompleter())

    def dummy_callback(self, *args, **kwargs):
        return

    def test_can_create_input_buffer(self):
        buffer = self.factory.create_input_buffer()
        self.assertEqual(buffer.name, 'input_buffer')

    def test_can_create_input_buffer_with_callback(self):
        buffer = self.factory.create_input_buffer(self.dummy_callback)
        self.assertTrue(buffer.on_text_changed is not None)

    def test_can_create_doc_buffer(self):
        buffer = self.factory.create_doc_buffer()
        self.assertEqual(buffer.name, 'doc_buffer')

    def test_can_create_input_buffer_container(self):
        buffer = mock.Mock(spec=Buffer)
        container = self.factory.create_input_buffer_container(buffer)
        self.assertTrue(container.content is not None)

    def test_can_create_doc_window(self):
        buffer = mock.Mock(spec=Buffer)
        container = self.factory.create_doc_window(buffer)
        self.assertTrue(container.content is not None)

    def test_can_create_search_field(self):
        search_field = self.factory.create_search_field()
        self.assertIsInstance(search_field, SearchToolbar)

    def test_can_create_layout(self):
        layout = self.factory.create_layout()
        self.assertTrue(layout.container is not None)

    def test_can_create_layout_with_input_buffer_callback_specified(self):
        layout = self.factory.create_layout(
            on_input_buffer_text_changed=self.dummy_callback)
        self.assertTrue(layout.container is not None)

    def test_can_create_layout_with_input_buffer_container_specified(self):
        layout = self.factory.create_layout(input_buffer_container=Window())
        self.assertTrue(layout.container is not None)

    def test_can_create_layout_with_doc_window_specified(self):
        layout = self.factory.create_layout(doc_window=Window())
        self.assertTrue(layout.container is not None)

    def test_can_create_layout_with_search_field_specified(self):
        search_field = SearchToolbar()
        layout = self.factory.create_layout(search_field=search_field)
        self.assertTrue(layout.container is not None)

    def test_can_create_key_bindings(self):
        key_bindings = self.factory.create_key_bindings()
        self.assertIsInstance(key_bindings, PromptToolkitKeyBindings)


class TestCLIPromptBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = CLIPromptBuffer()

    def test_history_mode_switching(self):
        self.buffer.switch_history_mode()
        self.assertIsInstance(self.buffer.completer, HistoryCompleter)
        self.buffer.switch_history_mode()
        self.assertIsInstance(self.buffer.completer, Completer)

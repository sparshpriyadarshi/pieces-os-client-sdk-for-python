import unittest
from queue import Queue
from unittest.mock import Mock, patch
from pieces_os_client import (
    QGPTStreamEnum,
)
from pieces_os_client.wrapper.websockets import AskStreamWS
from pieces_os_client.wrapper.copilot import Copilot
from pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from pieces_os_client.wrapper.streamed_identifiers.conversations_snapshot import ConversationsSnapshot

class BasicCopilotTest(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.mock_client.tracked_application = Mock(id="mock_app_id")
        self.mock_client.model_id = "mock_model_id"
        self.mock_client.qgpt_api = Mock()
        
        # Define a real BasicChat class for testing
        global BasicChat
        class BasicChat:
            def __init__(self, id):
                self.id = id
        
        self.copilot = Copilot(self.mock_client)

        # Mock ConversationsSnapshot
        self.mock_conversations = patch('__main__.ConversationsSnapshot.identifiers_snapshot', {"test_conversation_id": Mock()}).start()

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertIsInstance(self.copilot, Copilot)
        self.assertEqual(self.copilot.pieces_client, self.mock_client)
        self.assertIsInstance(self.copilot._on_message_queue, Queue)
        self.assertIsInstance(self.copilot.ask_stream_ws, AskStreamWS)
        self.assertIsNone(self.copilot._chat)

    @patch('__main__.AskStreamWS')
    def test_ask(self, mock_ask_stream_ws):
        query = "Test query"
        mock_output = Mock(status=QGPTStreamEnum.COMPLETED, conversation="test_conversation_id", text="Test response")
        self.copilot._on_message_queue.put(mock_output)
        
        # Create a mock for send_message
        mock_send_message = Mock()
        self.copilot.ask_stream_ws.send_message = mock_send_message
        
        result = list(self.copilot.ask(query))
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_output)
        self.assertIsInstance(self.copilot.chat, BasicChat)
        self.assertEqual(self.copilot.chat.id, "test_conversation_id")
        
        # Assert that send_message was called once
        mock_send_message.assert_called_once()

    def test_question(self):
        query = "Test question"
        mock_output = Mock(text="Test answer", answers=[])
        self.mock_client.qgpt_api.question.return_value = mock_output
        
        result = self.copilot.question(query)
        
        self.assertEqual(result, mock_output)
        self.mock_client.qgpt_api.question.assert_called_once()

    def test_chats(self):
        ConversationsSnapshot.identifiers_snapshot = {"chat1": Mock(), "chat2": Mock()}
        chats = self.copilot.chats()
        
        self.assertEqual(len(chats), 2)
        self.assertIsInstance(chats[0], BasicChat)
        self.assertIsInstance(chats[1], BasicChat)

    def test_chat_property(self):
        self.assertIsNone(self.copilot.chat)
        
        test_chat = BasicChat("test_conversation_id")
        self.copilot.chat = test_chat
        self.assertEqual(self.copilot.chat, test_chat)
        
        with self.assertRaises(ValueError):
            self.copilot.chat = "invalid_chat"

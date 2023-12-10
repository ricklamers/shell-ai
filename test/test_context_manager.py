import unittest
from shell_ai.code_parser import _ContextManager, ContextManager, MAX_CONTEXT_TOKENS

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.ctx_manager = ContextManager

    def test_add_token(self):
        self.ctx_manager.add_token('token1')
        self.assertEqual(len(self.ctx_manager.token_buffer), 1)
        self.assertEqual(self.ctx_manager.token_buffer[0], 'token1')
        self.ctx_manager.flush()

    def test_add_chunk(self):
        chunk = ['chunk', 'of', 'tokens']
        self.ctx_manager.add_chunk(chunk)
        buffer_list = list(self.ctx_manager.token_buffer)
        self.assertEqual(len(buffer_list), len(chunk))
        self.assertEqual(buffer_list[-len(chunk):], chunk)
        self.ctx_manager.flush()

    def test_get_ctx(self):
        tokens = ['token' + str(i) for i in range(MAX_CONTEXT_TOKENS + 100)]
        self.ctx_manager.add_chunk(tokens)
        expected_ctx = ''.join(tokens[-MAX_CONTEXT_TOKENS:])
        self.assertEqual(self.ctx_manager.get_ctx(), expected_ctx)
        self.ctx_manager.flush()

    def test_singleton_instance(self):
        new_ctx_manager = _ContextManager()
        self.assertIs(self.ctx_manager, new_ctx_manager)


if __name__ == '__main__':
    unittest.main()

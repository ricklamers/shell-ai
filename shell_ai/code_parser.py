import mistune
from collections import deque

MAX_CONTEXT_TOKENS = 1500

class PythonCodeBlockParser(mistune.HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super(PythonCodeBlockParser, self).__init__(*args, **kwargs)
        self.code_blocks = []
        self.codespans = []

    def codespan(self, code):
        self.codespans.append(code)
        return super().codespan(code)

    def block_code(self, code, info=None):
        #lang = info.split(None, 1)[0] if info else None
        self.code_blocks.append(code)
        return super().block_code(code)

class _ContextManager:
    """
    Store console outputs in context mode.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.max_tokens = MAX_CONTEXT_TOKENS
            cls._instance.token_buffer = deque(maxlen=MAX_CONTEXT_TOKENS)
        return cls._instance

    def add_token(self, token):
        self.token_buffer.append(token)
    
    def flush(self):
        self.token_buffer.clear()
    
    def add_chunk(self, chunk):
        self.flush()
        for c in chunk:
            self.add_token(c)

    def get_ctx(self):
        if len(self.token_buffer) == 0:
            return ''
        return ''.join(list(self.token_buffer))

ContextManager = _ContextManager()

def code_parser(markdown):
    """
    This returns either the joined code_blocks
    and iff no code_blocks are found we return the
    joined codespans, if those are also empty we return
    the full markdown output as if it's code.
    """
    renderer = PythonCodeBlockParser()
    parser = mistune.create_markdown(renderer=renderer)
    parser(markdown)

    if renderer.code_blocks:
        return "".join(renderer.code_blocks)
    if renderer.codespans:
        return "\n".join(renderer.codespans)
    return markdown 
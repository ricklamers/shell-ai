import mistune


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
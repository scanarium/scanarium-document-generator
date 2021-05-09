import markdown


class MarkdownRenderer(object):
    def render(self, text):
        return markdown.markdown(text, extensions=['extra'])

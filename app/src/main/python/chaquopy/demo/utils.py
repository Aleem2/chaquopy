from io import StringIO
from os.path import join


# Passes each write to the underlying stream, and also to the given method (which must take a
# single String argument) on the given Java object.
class JavaTeeOutputStream(StringIO):
    def __init__(self, stream, obj, method):
        StringIO.__init__(self)
        self.stream = stream
        self.func = getattr(obj, method)

    def write(self, s):
        self.stream.write(s)
        self.func(s)

    def flush(self):
        self.stream.flush()


ASSET_SOURCE_DIR = "source"
EXTRA_CSS = "body { background-color: #eeeeee; font-size: 85%; }"

# Compare with the equivalent Java code in JavaDemoActivity.java
def view_source(context, web_view, filename):
    from base64 import b64encode
    from java.io import BufferedReader, InputStreamReader
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_for_filename

    stream = context.getAssets().open(join(ASSET_SOURCE_DIR, filename))
    reader = BufferedReader(InputStreamReader(stream))
    text = "\n".join(iter(reader.readLine, None))

    formatter = HtmlFormatter()
    body = highlight(text, get_lexer_for_filename(filename), formatter)
    html = ("<html><head><style>{}\n{}</style></head><body>{}</body></html>"
            .format(formatter.get_style_defs(), EXTRA_CSS, body)).encode()
    web_view.loadData(b64encode(html).decode(), "text/html", "base64")
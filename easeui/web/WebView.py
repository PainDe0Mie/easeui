import urllib.request
from .HtmlViewer import HtmlViewer

class WebView:
    def __init__(self, root, url):
        self.root = root
        self.url = url

    def open(self):
        try:
            response = urllib.request.urlopen(self.url)
        except:
            print("Your link doesn't work. " + self.url)

        data = response.read()
        html = data.decode("ISO-8859-1")

        HtmlViewer(self.root, html, self.url).render()
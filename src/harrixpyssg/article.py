import harrixpylib as h


class Article:
    """All information about an article.

    Extended description of class

    Attributes:
        attr1 (int): Description of attr1
        attr2 (str): Description of attr2
    """
    def __init__(self):
        self.md = ""
        self.meta = dict()
        self.html = ""
        self.path_html = ""
        self.featured_image = None
        self.attribution = None

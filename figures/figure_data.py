class FigureData:
    def __init__(self, cls, *args, **kw):
        self.cls = cls
        self.args = args
        self.kw = kw

    def get_figure(self):
        return self.cls(*self.args, **self.kw)
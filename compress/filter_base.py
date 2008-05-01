class FilterBase:
    def __init__(self, verbose):
        self.verbose = verbose

    def filter_css(self, css):
        raise NotImplementedError
    def filter_js(self, js):
        raise NotImplementedError
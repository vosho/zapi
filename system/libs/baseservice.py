class BaseService:
    ctx = None
    application = None
    auto_load = True
    is_debug = False

    def init(self, cfg = None):
        pass

    def set_debug(self, debug):
        self.is_debug = debug

class BaseContext:
    ctx = None
    params = []

    def set_params(self, params):
        self.params = params

    def get_param(self, index):
        if index >= len(self.params):
            return None
        else:
            return self.params[index]

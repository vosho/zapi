from system.libs.restcontroller import RestController


class IndexController(RestController):
    def init(self):
        self.ctx.load_service('db')

    def get_index(self):
        pass

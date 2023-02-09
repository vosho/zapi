from system.libs.kit import Kit
from system.libs.restcontroller import RestController


class DemoController(RestController):
    def OPTIONS(self):
        pass
    def post_task(self):
        self.make_result({})
    def get_index(self):
        self.make_result({})
    def get_random(self):
        self.make_result({'code': Kit.rand_int(10000, 900000)})

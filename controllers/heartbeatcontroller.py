from system.libs.restcontroller import RestController


class HeartbeatController(RestController):
    def prepare(self):
        self.ctx.load_service('db')
        pass

    def get_index(self):
        MyIpc = self.ctx.services.db.load_model('ipc', 'mysql')
        self.make_result({
            "msg": 'msg from api'
        })

from system.libs.restcontroller import RestController


class LoginController(RestController):
    def prepare(self):
        super().prepare()

    def get_index(self):
        MqConfig = self.ctx.services.db.load_model('Config', self.ctx.cfg.env)
        config_list = MqConfig.get_all()
        print(config_list.count())
        return self.make_result({})

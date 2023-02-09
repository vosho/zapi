import logging

from system.libs.apicontroller import ApiController


class RestController(ApiController):
    name = None
    model = None

    def prepare(self):
        super().prepare()

        self.name = type(self).__name__
        clz_name = self.name.replace('Controller', '').lower()

        modelClass = clz_name.capitalize()
        try:
            self.model = self.ctx.services.db.load_model(modelClass)
        except Exception as e:
            logging.exception(f'{clz_name} not found')
        self.before()

    def before(self):
        pass

    def get_list(self):
        if not self.name:
            return
        data = self.model.get_all()
        self.make_pager_result(data)

    def post_save(self):
        pdata = self.get_data()
        site = self.model.save_from_data(pdata)
        self.make_pager_result(site)

    def get_info(self):
        pdata = self.validate(['id'])
        find = self.model.get_one_or_none(self.model.id == pdata['id'])
        self.make_result(find)

    def post_delete(self):
        pdata = self.validate(['id'])
        self.model.delete_with(self.model.id == pdata['id'])
        self.make_msg('Delete Successfully')
    def check_login(self):
        is_login = 'is_login' in self.session and self.session['is_login'] == True
        if not is_login:
            self.make_login('Sign in first')

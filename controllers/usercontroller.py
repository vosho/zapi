from libs.mybasecontroller import MyBaseController


class UserController(MyBaseController):
    @auth.login
    def get_list(self):
        self.make_result({
            'list': [1,2,3,4]
        })
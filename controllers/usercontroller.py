from libs.mybasecontroller import MyBaseController


class UserController(MyBaseController):
    def get_list(self):
        self.make_result({
            'list': [1,2,3,4]
        })
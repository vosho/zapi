import logging

from system.libs.restcontroller import RestController


class MyBaseController(RestController):
    def before(self):
        super(MyBaseController, self).before()
        if self.name != 'UserController' or self.name != 'DemoController':
            self.check_login()
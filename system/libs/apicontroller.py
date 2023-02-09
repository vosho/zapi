from system.libs.basecontroller import BaseController


class ApiController(BaseController):
    def get_data(self):
        if self.request.method == 'POST':
            query_data = self.get_post_json()
        else:
            query_data = self.get_param_data()
        return query_data

    def validate(self, fields):
        missings = []
        pdata = self.get_data()
        for f in fields:
            if f not in pdata or pdata[f] is None:
                missings.append(f)
        msg = None
        if len(missings):
            msg = ','.join(missings) + ' missing'
            self.make_alert(msg)
            self.end()

        return pdata

    def encrypt(self, s):
        return s

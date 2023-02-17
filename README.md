
# ZAPI  
ZAPI is Simple Fast Python MVC Framework, based on tornado, and peewee database orm.


## Acknowledgements

 - [Tornado](https://www.tornadoweb.org/en/stable/)
 - [Peewee](http://docs.peewee-orm.com/en/latest/)


##  Features
- MVC framework, models, views, controllers
- Dynamic routing: routing reflects to controllers, with prefix methods
- Task Integration: tasks with models. See `Tasks`
- Testing Framework: Unitesting framework.

##  Structure

### Project has following structure 

```
.
└── ZAPI/
    ├── controllers/
    │   ├── indexcontroller.py
    │   └── democontroller.py
    ├── interceptors/
    │   └── dbinterceptor.py    
    ├── services/
    │   ├── dbservice.py
    │   ├── redisservice.py
    │   └── mqservice.py    
    ├── tasks/
    │   ├── demotask.py
    │   └── testtask.py
    ├── tests/
    │   └── demotest.py
    ├── views/
    │   ├── index.html
    │   └── assets/
    │       ├── js/
    │       │   └── index.js
    │       └── css/
    │           └── index.css
    ├── logs/
    │   └── ...
    ├── libs/
    │   └── basecontroller.py
    ├── runtask.sh
    ├── runtest.sh
    ├── config.json
    ├── main.py
    └── server.py
```
## Get Started

## Controllers
> For Example, `usercontroller.py` under folder `controllers`
```
.
└── ZAPI/
    └── controllers/
        └── usercontroller.py
```
#### File content
```python
from libs.mybasecontroller import MyBaseController

class UserController(BaseController):
    def get_list(self):
        self.make_result({
            'list': [1,2,3,4]
        })
```

#### Check result:
By default, browser: [http://127.0.0.1:3001/api/v1/user/list](http://127.0.0.1:3001/api/v1/user/list)
> Note: the `api/v1` is api `prefix`. it can be configured in `config.json`<br />
> Note: the **port** `3001` could be configured in `config.json`

## Models
Models are located in folder with suffix `model`<br>
For example, for `postgresql` models, the folder is `pgmodel`, and `MySQL` is `mqmodel`.

#### Example
```python
from peewee import IntegerField, CharField
from system.libs.basemodel import BaseModel

class MqUser(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    description = CharField(max_length=255)

    class Meta:
        db_table = 'user'
```

## Views
Views are mapped into folders `/views`

## Run Server
`python3 server.py`

## Tasks
ZApi enables user to run task integrated with framework features<br />
Tasks are located in folder `/tasks`

For example:
Task file `/tasks/demotask.py`<br />
File Content:
```python
from system.libs.basetask import BaseTask
class DemoTask(BaseTask):
    def run(self):
        print('this is a demo task')
```
#### Run Task:
`./runtask.sh demo`

## Configurations

#### Example.json
```json
{
  "prefix": "api/v1",
  "server": {
    "port": 3100
  },
  "env": "db_evn_name",
  "dbsource": {
    "db_evn_name": {
      "type": "mysql",
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "123456",
      "db": "aibox"
    }
  }
}
```

### License
MIT
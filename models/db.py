# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get('db.uri'), 
             pool_size = myconf.get('db.pool_size'),
             migrate_enabled = myconf.get('db.migrate'),
             check_reserved = ['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

db = DAL("sqlite://storage.sqlite")
from gluon.tools import Auth, Service, PluginManager,Crud

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db)
crud = Crud(db)
service = Service()
plugins = PluginManager()

db.define_table(auth.settings.table_user_name,
                Field('first_name', length=128, default=''),
                Field('last_name', length=128, default=''),
                Field('username', length=128, default='',unique=True),
                Field('email', length=128, default='', unique=True),
                Field('password', 'password', length=512,readable=False, label='Password'),
                Field('registration_key', length=512,writable=False, readable=False, default=''),
                Field('reset_password_key', length=512,writable=False, readable=False, default=''),
                Field('registration_id', length=512,writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.username.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=8,upper=1,lower=1,special=1), CRYPT()]
custom_auth_table.username.requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,custom_auth_table.username)]
custom_auth_table.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table



## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'md.raihan1710@gmail.com'
mail.settings.login = 'md.raihan1710:88d7fc621'


## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db = DAL('sqlite://db.db')
STATUSSES=('assigned','completed','pending')
NUMB=(0,10,20,30,40,50,60,70,80,90,100)
db.define_table('upload',
                Field('Task','text',requires=IS_NOT_EMPTY() and IS_NOT_IN_DB(db,'upload.Task')),
                Field('Username','text', readable=False, writable=False, requires = IS_NOT_EMPTY()),
                Field('Date_of_Upload', readable=False, writable=False, requires = IS_NOT_EMPTY()),
                Field('Description','text'),
                Field('Deadline','datetime',requires=IS_NOT_EMPTY()),
                #Field('Access','list:string',requires=IS_IN_SET(('public','private'))), 
                Field('status',requires=IS_IN_SET(STATUSSES),default=STATUSSES[0]),
                Field('complete_percent','integer',requires=IS_IN_SET(NUMB),default=NUMB[0]),
                #Field('email','text',requires=IS_EMAIL()),
                #Field('head',default=auth.user_id),##error is due to this line in task====requires=IS_IN_DB(db,upload.Username)
                #Field('head',db.auth_user),
                Field('SubTasks','boolean'),
                Field('SubTask1','text'),
                Field('SubTask2','text'),
                Field('SubTask3','text'),
                Field('SubTask4','text'),
                Field('SubTask5','text'),
                )
##db.upload.id.readable = False
db.define_table('post',
    Field('upload', readable=False, writable=False),
    Field('body', 'text'),
    Field('created_on', readable=False, writable=False),
    Field('created_by', readable=False, writable=False)
               )
db.define_table('addpers',
                Field('refs','integer',readable=False),
                Field('nmes','string',required=True,label="Name")
                )

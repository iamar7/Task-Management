# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import datetime
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    auth.settings.login_next=URL('incomplete')
    return dict(form=auth())
def show1():
    data = request.args(0)
    id=request.args(0,cast=int)
    rows = db(db.upload.id==data).select()
    po = db(db.upload.id==data).select().first()
    que=str(po.Date_of_Upload)
    db.post.upload.default = id
    db.post.created_on.default = request.now.date()
    db.post.created_by.default = auth.user.username
    form = SQLFORM(db.post).process(next='show1/[id]') if auth.user else None
    comments = db(db.post.upload==id).select()
    lists=db(db.addpers.refs==data).select(db.addpers.ALL,orderby=db.addpers.nmes)
    return locals()
    #return locals()
@auth.requires_membership('manager')
def manage():
    grid=SQLFORM.grid(db.upload)
    return locals()
    
@auth.requires_login()
def edit():
    if(auth.user==None):
        session.flash=("Please Login First")
    data=request.args(0,cast=int)
    form=SQLFORM(db.upload,data,deletable=True).process(next='show1/[data]')
    form.element('textarea[name=Task]')['_style']= 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=Description]')['_style']= 'font-size:20px;width:450px;height:60px;'
    if form.process().accepted:
		response.flash = 'form accepted'
    elif form.errors:
		response.flash = 'form has errors'
    return dict(data=data, form=form)
@auth.requires_login()
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
@auth.requires_login()
def task():
    if(auth.user==None):
        session.flash=("Please Login First")
    db.upload.complete_percent.writable= False
    db.upload.complete_percent.readable = False
    db.upload.status.writable = False
    db.upload.status.readable = False
    form=SQLFORM(db.upload)
    form.vars.Username=auth.user.username
    form.vars.Date_of_Upload=request.now.date()
    form.element('textarea[name=Task]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=Description]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    #form.element('textarea[name=Access])
    ##form.element('textarea[name=email]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=SubTask1]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=SubTask2]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=SubTask3]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=SubTask4]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('textarea[name=SubTask5]')['_style'] = 'font-size:20px;width:450px;height:60px;'
    form.element('[name=Deadline]')['_style'] = 'font-size:20px;width:450px;height:60px;'

    if form.process().accepted:
        response.flash= 'form accepted'
        redirect(URL('emailing'))
    return dict(form=form)
def emailing():
    mail.send(to=[auth.user.email],
              subject='Task created',
              message='Your task has been created'
              )
    session.flash=("email sent")
    redirect(URL('incomplete'))
              
@auth.requires_login()
def sub():
    form=SQLFORM(db.subt).process()
    if form.process().accepted: redirect(URL('task'))
    return locals()
def taggedtasks():
    sel=db(db.addpers.nmes==auth.user.username).select(db.addpers.ALL)
    for i in sel :
        news=db(db.upload.id==i['refs']).select(db.upload.ALL)
    return locals()
@auth.requires_login()
def incomplete():
    if (auth.user==None):
        session.flash = ("Please Login First")
    row=db(db.upload.Username==auth.user.username).select()
    b=request.args(0)
    query=(db.upload.Username==auth.user.username)
    c=db(query).count()
    current=datetime.datetime.now()
    if(b==None):
        i=0
    
    if(b!=None):
        i=int(b)
        
    if(c-i>5 and i>=0):
        rows=db(db.upload.Username==auth.user.username).select(orderby=~db.upload.id,limitby=(i,i+5))
    elif(i>=c):
        if(c%5!=0):
            i=5*int(c/5)
        else:
            i=15*(int(c/5)-1)
        rows=db(db.upload.Username==auth.user.username).select(orderby=~db.upload.id,limitby=(i,c))
    elif(i<0):
        i=0
        rows=db(db.upload.Username==auth.user.username).select(orderby=~db.upload.id,limitby=(0,5))
    else:
        rows=db(db.upload.Username==auth.user.username).select(orderby=~db.upload.id,limitby=(i,c))
    return locals()
    #return dict(rows=rows, c=c, i=i, b=b)
    #return dict(rows=rows)

@auth.requires_login()
def home():
    if (auth.user==None):
        session.flash = ("Please Login First")
        '''redirect("http://127.0.0.1:8000/cooking/default/user/login")'''
    b=request.args(0)
    query=(db.upload.id>0)
    c=db(query).count()
    if (b==None):
        i=0

    if (b!=None):
        i=int(b)
        #c=c-3
    if (c-i>5 and i>=0):
        rows = db(db.upload.Username!=None).select(orderby=~db.upload.id, limitby=(i,i+5))
    elif (i>=c):
        if (c%5!=0):
            i=5*int(c/5)
        else:
            i=5*(int(c/5)-1)
        rows = db(db.upload.Username!=None).select(orderby=~db.upload.id, limitby=(i,c))
    elif (i<0):
        i=0
        rows = db(db.upload.Username!=None).select(orderby=~db.upload.id, limitby=(0,5))
    else:
        rows = db(db.upload.Username!=None).select(orderby=~db.upload.id, limitby=(i,c))
    return dict(rows=rows, c=c, i=i, b=b)
def addperson():
    s=request.args(0,cast=int)
    seb=SQLFORM(db.addpers)
    seb.vars.refs=s
    if (seb.process().accepted):
        redirect(URL('home'))
        session.flash="Successful"
    else:
        response.flash="Try Again"
    return locals()
def update():
    id=request.args(0,cast=int)
    alpha=db.upload(id)
    another=request.args(1,cast=int)
    x=request.now<alpha.Deadline
    if((another==auth.user.id)&(alpha.status=='assigned')|(alpha.status =='pending')&(x==True)):
        db.upload.howmuch.writable = True
        db.upload.status.writable = True
        db.upload.status.readable = True
        db.upload.Deadline.readable = False
        db.upload.Deadline.writable = False
        db.upload.status.requires=IS_IN_SET(('completed','pending'))
        form=SQLFORM(db.upload,id,showid=False).process()
        if form.accepted:
            session.flash="Updated"
            redirect(URL('incomplete'))
    else:
            session.flash="NOT POSSIBLE"
            redirect(URL('home'))
    return locals()
def search():
     return dict(form1=FORM(INPUT(_id='keyword1',_name='keyword1', _onkeyup="ajax('callback1', ['keyword1'], 'target1');")),
target_div1=DIV(_id='target1'),form2=FORM(INPUT(_id='keyword2',_name='keyword2', _onkeyup="ajax('callback2', ['keyword2'], 'target2');")),target_div2=DIV(_id='target2'))
    
def callback1():
    if not request.vars.keyword1: return ' '
    query=db.upload.Task.startswith(request.vars.keyword1)
    projects=db(query).select(orderby=db.upload.Task)
    links=[A(p.Task,_href=URL('home',args=p.id)) for p in projects]
    return UL(*links)
def callback2():
    if not request.vars.keyword2: return ' '
    query1=db.auth_user.first_name.startswith(request.vars.keyword2)
    #query2=db.auth_user.last_name.startswith(request.vars.keyword2)
    q2=db.auth_user.id==db.upload.created_by
    projects=db(query1).select(db.upload.ALL,orderby=db.upload.Task)
    links=[A(p.Task,_href=URL('home',args=p.id)) for p in projects]
    return UL(*links)

    
'''def activity():
    db.upload.Deadline.represent = lambda x,row:prettydate(x)
    db.upload.Task.represent = lambda title,row:A(title,_href=URL('update',args=[row.id, row.head.id]))
    query=(db.upload.head == auth.user_id)
    grid=SQLFORM.grid(query, create=False, deletable=False, editable=False, fields=[db.upload.Task,db.upload.head,db.upload.status,db.upload.Deadline])
    return locals()
#db.upload.Deadline.represent = lambda x,row: prettydate(x)
def needtodo():
    #grid=SQLFORM.smartgrid(db.auth_user,linked_tables=['task'])
    rows=db((db.upload.status == 'assigned')|(db.upload.status == 'pending')).select(orderby=~db.upload.created_on)
    return locals()

def activitytable():
    s=db(db.upload.Username==(auth.user.first_name+auth.user.last_name)).select(db.upload.ALL)
    current=datetime.datetime.now()
    return locals()'''

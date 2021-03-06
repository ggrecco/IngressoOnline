#MODULOS
from bottle import *
from functools import wraps
import logging
from datetime import datetime
import os
import bcrypt
from beaker.middleware import SessionMiddleware
# OBJETOS
from model.usuario import Usuario
from model.conta import Conta
from model.evento import Evento
from model.carrinho import Carrinho
from model.ingresso import Ingresso
from model.categoria import Categoria
from model.ibge import IBGE


logger = logging.getLogger('IngressoOnline')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('IngressoOnline.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_to_logger(fn):
	@wraps(fn)
	def _log_to_logger(*args, **kwargs):
		request_time = datetime.now()
		actual_response = fn(*args, **kwargs)
		logger.info('%s %s %s %s %s' % (request.remote_addr,request_time,request.method,request.url,response.status))
		return actual_response
	return _log_to_logger

install(log_to_logger)	
TEMPLATE_PATH.insert(0,"view")
_session_opts = {'session.type':'memory','_session.cookie_expires':600,'_session.auto': True}
#_session_opts = {'session.type': 'file','session.data_dir': '/openmining.data','session.lock_dir': '/openmining.lock','session.cookie_expires': 5000,'session.auto': True}
app = SessionMiddleware(app(), _session_opts)

def has_session():
	_session = request.environ.get('beaker.session')
	if not _session or 'usuario_id' not in _session:
		return redirect('/login')

def set_session(key,value):
	_session = request.environ['beaker.session']
	_session[key] = value
	_session.save()
def del_session():
	_session = request.environ['beaker.session']
	_session.delete()

def get_session():
	try:
		_session = request.environ['beaker.session']
		return _session['usuario_id']
	except Exception:
		return 0

def check_password(passw,passwh):
	if bcrypt.hashpw(passw.encode(),passwh.encode()) == passwh:
		return True
	return False
def set_passwh(passw):
	return bcrypt.hashpw(passw.encode(),bcrypt.gensalt())

@route('/logout')
def logout_get():
	del_session()
	return redirect("/")

@route('/',method='GET')
def main_page():
	usuario_id = get_session()
	return template('view/index',usuario_id=usuario_id)

@route('/static/<filename:path>')
def static_routes(filename):
	return static_file(filename, root='static')

@error(404)
def error404(error):
	return template('view/404')

# Usuario Begin
@route('/usuario/profile',method='GET')
def usuario_profile_get(): 
	has_session()
	usuario_id = get_session()
	dado = Conta().find(usuario_id)
	return template('view/usuario/profile',dado=dado)

@route('/usuario/register',method='POST')
def usuario_register_post():		
	nome = request.POST.nome
	email = request.POST.email
	senha = request.POST.senha
	senha2 = request.POST.senha2	
	cpf = request.POST.cpf
	telefone = request.POST.telefone
	data_criacao = str(datetime.now())[0:19]

	if senha != senha2:
		return redirect(request.path)
	senha = set_passwh(senha)
		
	if Usuario().add(email,senha):
		usuario_id = Usuario().find_by_email(email)[0]
		if Conta().add(usuario_id,nome,cpf,telefone,data_criacao):
			set_session('usuario_id',usuario_id)
	return redirect("/")


@route('/usuario/register',method='GET')
def usuario_register_get():
	return template('view/usuario/register')

@route('/usuario/edit',method='POST')
def usuario_edit_post():
	has_session()
	nome = request.POST.nome
	email = request.POST.email
	cpf = request.POST.cpf
	telefone = request.POST.telefone
	usuario_id  = get_session()
	data_alteracao = str(datetime.now())[0:19]
	if Usuario().update(email,usuario_id):
		if Conta().update(nome,cpf,telefone,data_alteracao,usuario_id):
			return redirect("/usuario/profile")
	return redirect("/")

@route('/usuario/edit',method='GET')
def usuario_edit_get():
	has_session()
	usuaario_id = get_session()
	dado = Conta().find(get_session())
	return template('view/usuario/edit',dado=dado)

@route('/usuario/delete',method='POST')
def usuario_delete_post():
	has_session()
	usuario_id = get_session()
	if Usuario().delete(usuario_id):
		del_session()	
	return redirect('/')

@route('/usuario/delete',method='GET')
def usuario_delete_get():
	has_session()
	usuario_id = get_session()
	dados = Conta().find(usuario_id)
	return template('view/usuario/delete', dados=dados)

@route('/login',method='POST')
def usuario_login_post():
	email = request.POST.email
	senha = request.POST.senha
	dado = Usuario().find_by_email(email)
	if check_password(senha,dado[2]):
		set_session('usuario_id',dado[0])
		return redirect('/')
	return redirect(request.path)

@route('/login',method='GET')
def usuario_login_get():
	return template('view/usuario/login')

@route('/usuario/reset',method='POST')
def reset_password_get():
	has_session()
	senha_atual = request.POST.senha_atual
	nova_senha = request.POST.nova_senha
	nova_senha2 = request.POST.nova_senha2
	if nova_senha != nova_senha2:
		return redirect(request.path)

	usuario_id = get_session()
	dado = Usuario().find(usuario_id)
	if not check_password(senha_atual,dado[2]):
		return redirect(request.path)

	nova_senha = set_passwh(nova_senha)
	if Usuario().reset_password(nova_senha,get_session()):
		return redirect('/')

	return redirect(request.path)

@route('/usuario/reset',method='GET')
def reset_password_get():
	has_session()
	return template('view/usuario/reset_password')
# Usuario end
# Ingresso begin

@route('/ingresso',method='GET')
@route('/ingresso/index',method='GET')
def ingresso_index_get():
	has_session()
	usuario_id = get_session()
	dado = Ingresso().findAll(usuario_id)
	return template('view/ingresso/index',dado=dado)
@route('/ingresso/insert',method='POST')
def ingresso_insert_post():
	has_session()
	tipo = request.POST.tipo
	quantidade = request.POST.quantidade
	preco = request.POST.preco
	evento_id = request.POST.evento_id
	usuario_id = get_session()
	if Ingresso().add(tipo,quantidade,preco,usuario_id,evento_id):
		return redirect('/ingresso')
	return redirect('/ingresso/insert')

@route('/ingresso/insert',method='GET')
def ingresso_insert_get():
	has_session()
	usuario_id = get_session()
	evento = Evento().findAll(usuario_id)
	return template('view/ingresso/insert',evento=evento)

@route('/ingresso/edit/<_id>',method='POST')
def ingresso_edit_post(_id):
	has_session()
	tipo = request.POST.tipo
	quantidade = request.POST.quantidade
	preco = request.POST.preco
	usuario_id = get_session()

	if Ingresso().update(tipo,quantidade,preco,usuario_id,_id):
		return redirect('/ingresso')
	return redirect('/ingresso/edit/'+_id)

@route('/ingresso/edit/<_id>',method='GET')
def ingresso_edit_get(_id):
	has_session()
	usuario_id = get_session()
	dado = Ingresso().find(usuario_id,_id)
	print dado
	return template('view/ingresso/edit',dado=dado)

@route('/ingresso/delete/<_id>',method='GET')
def ingresso_delete_get(_id):
	has_session()
	usuario_id = get_session()
	if Ingresso().delete(usuario_id,_id):
		return redirect('/ingresso')
	return redirect('/')
#Ingresso end
#Evento begin
@route('/evento/upload', method='POST')
def evento_upload_post():
	has_session()
	usuario_id = get_session()
	upload = request.files.get('upload')
	name, ext = os.path.splitext(upload.filename)
	file_path = save_path+"/"+upload.filename
	
	if ext not in ('.png', '.jpg', '.jpeg'):
		return "File extension not allowed."
	save_path = "EventoImage/"+usuario_id
	if not os.path.exists(save_path):
		os.makedirs(save_path)

	
	upload.save(file_path)
	return "File successfully saved"

@route('/evento/upload', method='GET')
def evento_upload_get():
	has_session()
	return template('view/evento/upload')

@route('/evento/<_id>', method='GET')
def page_evento_get(_id):
	dado = Evento().find_by_evento_id(_id)
	ingresso = Ingresso().find_by_evento_id(_id)
	return template('view/evento/show',dado=dado,ingresso=ingresso)
	

@route('/list-event', method='GET')
def evento_list_get():
	evento = Evento().listAll()
	categoria = Categoria().findAll()
	return template('view/evento/catalog',categoria=categoria,evento=evento)


@route('/evento', method='GET')
@route('/evento/index', method='GET')
def evento_index_get():
	has_session()
	usuario_id = get_session()
	dado = Evento().findAll(usuario_id)
	return template('view/evento/index',dado=dado)

@route('/evento/insert', method='POST')
def evento_insert_post():
	has_session()
	usuario_id = get_session()
	titulo = request.POST.titulo
	categoria_id = request.POST.categoria_id
	descricao = request.POST.descricao
	endereco = request.POST.endereco
	numero = request.POST.numero
	cidade_id = request.POST.cidade_id
	bairro = request.POST.bairro
	telefone = request.POST.telefone
	if Evento().add(usuario_id,categoria_id,cidade_id,titulo,descricao,endereco,numero,bairro,telefone):
		return redirect('/evento')
	return "Ocorreu um erro<a href='%s'>Go back</a>" % request.path

@route('/evento/insert', method='GET')
def evento_insert_get():
	has_session()
	cidade = IBGE().findAll() 
	categoria = Categoria().findAll()
	return template('view/evento/insert',categoria=categoria,cidade=cidade)
@route('/evento/edit/<_id>', method='POST')
def evento_edit_post(_id):
	has_session()
	usuario_id = get_session()
	titulo = request.POST.titulo
	categoria_id = request.POST.categoria_id
	descricao = request.POST.descricao
	endereco = request.POST.endereco
	numero = request.POST.numero
	cidade_id = request.POST.cidade_id
	bairro = request.POST.bairro
	telefone = request.POST.telefone
	if Evento().update(_id,usuario_id,categoria_id,cidade_id,titulo,descricao,endereco,numero,bairro,telefone):
		return redirect('/evento')
	print 'Error'
@route('/evento/edit/<_id>',method='GET')
def evento_edit_get(_id):
	has_session()
	usuario_id = get_session()
	dado = Evento().find(usuario_id,_id)
	cidade = IBGE().findAll() 
	categoria = Categoria().findAll()
	return template('view/evento/edit',cidade=cidade,categoria=categoria,dado=dado)

@route('/evento/delete/<_id>',method='GET')
def evento_delete_get(_id):
	has_session()
	usuario_id = get_session()
	if Evento().delete(usuario_id,_id):
		return redirect('/evento')
	return redirect('/')
#Evento end
#Shopping cart begin
@route('/carrinho/insert/<evento_id>/<ingresso_id>',method='POST')
def add_cart_get(evento_id,ingresso_id):
	has_session()
	quantidade = request.POST.quantidade
	usuario_id = get_session()
	if quantidade <= 0:
		quantidade = 1
	if Carrinho().add(ingresso_id,usuario_id,quantidade):
		pass	
	return redirect('/evento/%s' % evento_id)

@route('/carrinho/delete/<_id>',method='GET')
def carrinho_delete_get(_id):
	has_session()
	usuario_id = get_session()
	if Carrinho().delete(_id,usuario_id):
		return redirect('/carrinho')
	return redirect('/')
	
@route('/carrinho',method='GET')
def carrinho_index_get():
	has_session()
	usuario_id = get_session()
	dado = Carrinho().findAll(usuario_id)
	return template('view/carrinho/index.tpl',dado=dado)
#Shopping cart begin
run(host='127.0.0.1',port='8080',debug=True,reloader=True,app=app)

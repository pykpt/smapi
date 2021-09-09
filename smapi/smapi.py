import requests


class SchoolAPIError(Exception):
	pass


class APIBase:
	def __init__(self, token: str):
		self.session = requests.Session()
		self.session.headers = {'Access-Token': token}
		self.host = 'https://api.school.mosreg.ru/'
	
	def get(self, method: str, params={}, v='v2.0/'):
		return self.session.get(self.host + v + method, params=params).json()

	def post(self, method: str, data={}, v='v2.0/'):
		return self.session.post(self.host + v + method, data=data).json()

	def delete(self, method: str, params={}, v='v2.0/'):
		return self.session.delete(self.host + v + method, params=params).json()

	def put(self, method: str, data={}, v='v2.0/'):
		return self.session.put(self.host + v + method, data=data).json()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.close()


class Client(APIBase):
	def __init__(self, token: str = '', login: str = '', password: str = ''):
		if token != '':
			self.token = token
		if login != '' and password != '':
			self.token = self.get_token(login, password)
		super().__init__(self.token)
	
	def get_token(self, login, password):
		session = requests.Session()
		data = {"exceededAttempts":"False", "ReturnUrl":"", "login": login, "password": password, "Captcha.Input":"", "Captcha.Id":""}
		session.post("https://login.school.mosreg.ru/login", data=data)
		token = session.get(f'https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=').url
		if token[227:-53] == 'result=success':
			return token[255:-7]
		else:
			raise SchoolAPIError('Неудачная авторизация')
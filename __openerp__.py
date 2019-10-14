{
	'name': 'HR Auto User',
	'version': '0.1',
	'category': 'Human Resources',
	'description': """
		Automatically create user for every employee registered. Also add Employee ID (unique company-issued identifier).
	""",
	'author': 'Christyan Juniady and Associates',
	'maintainer': 'Christyan Juniady and Associates',
	'website': 'http://www.chjs.biz',
	'depends': ["base", "web", "hr"],
	'sequence': 150,
	'data': [
	],
	'demo': [
	],
	'test': [
	],
	'update_xml': [
		'views/hr_auto_user.xml'
	],
	'installable': True,
	'auto_install': False,
	'qweb': [
	]
}

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.modules import get_module_resource, get_module_path
import random

# ===============================================================================================================================

class hr_employee(osv.osv):
	
	_inherit = 'hr.employee'
	
# COLUMNS -----------------------------------------------------------------------------------------------------------------------

	_columns = {
		'employee_no': fields.char('Employee ID', size=50),
	}
	
# CUSTOM METHODS ----------------------------------------------------------------------------------------------------------------

	"""
	Gets employee ID of a user.
	
	@param userid: integer, the user ID requested. If empty, currently login user is used instead.
	@param with_data: boolean. If True, all employee data (result of .browse() call) is returned, otherwise it is just the id. 
	
	@return integer or browse_record on success, False otherwise.
	""" 
	def get_employee_id_from_user(self, cr, uid, userid=None, with_data=False):
	# ambil user tertentu tuh personnelnya yang mana?
		if userid == None: userid = uid # kalo user ngga kasih userid, maka diasumsikan ambil yang sekarang lagi login
		employee_id = self.search(cr, uid, [('user_id','=',userid)]) 
		if employee_id:
			if with_data:
				return self.browse(cr, uid, employee_id[0])
			else:
				return employee_id[0]
		else:
			return False
		
# OVERRIDES ---------------------------------------------------------------------------------------------------------------------

	def create(self, cr, uid, vals, context=None):
	# ketika create employee, sekaligus juga create user 
	#	- name == nama personnel
	#	- login == representasi lowercase + dot dari dua kata pertama name
		user_obj = self.pool.get("res.users")
	# cek apakah nama login user unik. generate angka random untuk di-suffix ke login name bila ada kasus tidak unik
		unique = False
		rand = ""
		while not unique:
			login = ".".join(vals['name'].split()[:2]).lower()+rand
			check = user_obj.search(cr, uid, [('login','=',login)])
			if not check: 
				unique = True
			else:
				rand = "%s" % random.randint(1,100)
	# barulah bikin usernya
		user_id = user_obj.create(cr, uid, {
			'name': vals['name'],
			'password': vals['employee_no'],
			'login': login,
			'active': True,
		})
	# update linkage dari employee ke user
		if user_id:
			vals.update({'user_id':user_id})
		return super(hr_employee, self).create(cr, uid, vals, context=context)

	def write(self, cr, uid, ids, vals, context=None):
		result = super(hr_employee, self).write(cr, uid, ids, vals, context=context)
	# ketika write employee, update juga name dan status active si user ybs
		if result and ('active' in vals or 'name' in vals):
			user_obj = self.pool.get("res.users")
			for row in self.browse(cr, uid, ids, context=context):
				if row.user_id:
					user_obj.write(cr, uid, row.user_id.id, { 'active': row.active, 'name': row.name })
		return result

	def unlink(self, cr, uid, ids, context=None):
		user_obj = self.pool.get("res.users")
	# hapus juga user ybs
		for row in self.browse(cr, uid, ids, context=context):
			if row.user_id:
				user_obj.unlink(cr, uid, [row.user_id.id], context)
		return super(hr_employee, self).unlink(cr, uid, ids, context)

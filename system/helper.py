from django.db import connection
import datetime


def convertStringToDate(str_date):
	date = datetime.datetime.strptime(str_date, "%d/%m/%Y")
	return date


def getUSR_ID(username):
	
	sql = "select usr_id from user_policy_mapping where username='" + str(username) + "'"
	cursor = connection.cursor()
	cursor.execute(sql)
	row = cursor.fetchone()
	cursor.close		

	if row is not None:
		usr_id = row[0]
	else:
		usr_id = None
	
	# print("username = " + str(username))
	# print('usr_id = ' + str(usr_id))

	return usr_id


def getPriority(usr_id, form_name):
	is_pass = False

	getPriorityStatus = False
	gUSE = False
	gADD = False
	gEDIT = False
	gDEL = False
	gPREVIEW = False
	gPRINT = False
	gIM = False
	gEX = False
	gSALARY = False
	gType = "A"
	gOLD = False
	
	# Get Module Name
	sql = "select mod_id,mod_type,mod_fre,mod_th,mod_en,con_type,mod_grp,frm_name,rep_name1,rep_name,paper,mod_sql,mod_into,mod_where,mod_table from module where frm_name='" + form_name + "'"	
	cursor = connection.cursor()	
	cursor.execute(sql)	
	module = cursor.fetchall()
	cursor.close()
	if len(module) == 1:
		MDL = module[0][0]
		gReport = module[0][9]
		gReport1 = module[0][8]
		is_pass = True
		getPriorityStatus = True
	else:
		MDL = ""
		gReport = ""
		gReport1 = ""
		getPriorityStatus = False
		is_pass = False

	# Get Policy
	if is_pass:
		sql = "select plc_id,ust_id,mod_id,plc_use,plc_add,plc_edit,plc_del,plc_preview,plc_print,plc_im,plc_ex,plc_salary,plc_type,plc_old,upd_date,upd_by,upd_flag,usr_id from policy where usr_id='" + str(usr_id) + "' and mod_id=" + str(MDL)
		cursor = connection.cursor()	
		cursor.execute(sql)	
		policy = cursor.fetchall()
		cursor.close()
		if len(policy) == 1:
			gUSE = policy[0][3]	#PLC_USE
			gADD = policy[0][4]	#PLC_ADD
			gEDIT = policy[0][5]	#PLC_EDIT
			gDEL = policy[0][6]	#PLC_DEL
			gPREVIEW = policy[0][7]	#PLC_PREVIEW
			gPRINT = policy[0][8]	#PLC_PRINT
			gIM = policy[0][9]	#PLC_IM
			gEX = policy[0][10]	#PLC_EX
			gSALARY = policy[0][11]	#PLC_SALARY
			gType = policy[0][12] if policy[0][12] != "" else "A"	#PLC_TYPE
			gOLD = True if policy[0][13] else False	#PLC_OLD
			gGROUP = policy[0][1]	#UST_ID
			gPERMIT = True if policy[0][1]=='SUV' else False
			if not gPERMIT:
				gPERMIT = True if policy[0][1]=='PSN' else False			

			if gType != "":
				message = ""
				# print("TODO: GetGaray()")

			getPrioity = True
		else:
			gUSE = False
			gADD = False
			gEDIT = False
			gDEL = False
			gPREVIEW = False
			gPRINT = False
			gIM = False
			gEX = False
			gSALARY = False
			gType = "A"
			gOLD = False
			getPrioity = False

	return getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD

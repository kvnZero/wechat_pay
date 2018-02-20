#coding=utf8
import itchat
import re
import time
from datetime import datetime
from sqlmodels import Order, User, Log, Goods, session
PRINT_LOG = True

def save_in_order(returnmsg):
	order = Order(fromuser=returnmsg['fromuser'], money=returnmsg['money'], createtime=returnmsg['createtime'], note=returnmsg['note'])
	_log = Log(douser=returnmsg['fromuser'], dowhat="%s in %s pay %s money." % (returnmsg['fromuser'], returnmsg['createtime'], returnmsg['money']), time = datetime.utcnow())
	session.add_all([order, _log])
	session.commit()

def add_in_user(returnmsg):
	user = session.query(User).filter_by(wechat_user=returnmsg['fromuser']).first()
	if user:
		old_money = user.money
		new_money = user.money + user.returnmsg['money']
		user.money = new_money
		user.lastmoney = old_money
		user.lastdotime = datetime.utcnow()
		_log = Log(douser=returnmsg['fromuser'], dowhat="%s recharge %s." % (returnmsg['fromuser'], returnmsg['money']), time = datetime.utcnow())
	else:
		user = User(user=returnmsg['fromuser'], wechat_user=returnmsg['fromuser'], money=returnmsg['money'], lastmoney="0", orders="", createtime=datetime.utcnow(), lastdotime=datetime.utcnow())
		_log = Log(douser=returnmsg['fromuser'], dowhat="%s create and recharge %s." % (returnmsg['fromuser'], returnmsg['money']), time = datetime.utcnow())
		session.add(user)
	session.add(_log)
	session.commit()

def buy_goods(returnmsg):
	if str(returnmsg['note']).isdigit():
		goods = session.query(Goods).filter_by(id=returnmsg['note']).first()
		goodsprice = goods.money
		getmoney = returnmsg['money']
		if goodsprice == getmoney:
			goods.quantity = goods.quantity-1
			_log = Log(douser=returnmsg['fromuser'], dowhat="%s buy %s." % (returnmsg['fromuser'], goods.name), time = datetime.utcnow())
			session.add(_log)
		else:
			add_in_user(returnmsg)
	session.commit()

@itchat.msg_register(itchat.content.SHARING)
def text_reply(msg):
	returnmsg = {}
	returnmsg['content'] = msg.Content

	try:
		returnmsg['fromuser'] = msg.fromUserName
		returnmsg['money'] = re.findall(re.compile(r'微信支付收款(.*?)元'), returnmsg['content'])[0]
		returnmsg['createtime'] = datetime.utcnow()
		returnmsg['note'] = re.findall(re.compile(r'付款方备注：(.*?)\n'), returnmsg['content'])[0]
	except IndexError:
		returnmsg['note'] = ""


	if returnmsg['note'] and returnmsg['money']:
		if PRINT_LOG:
			logstr = "From:%s, Money:%s, Note:%s, Time:%s" % (returnmsg['fromuser'], returnmsg['money'], returnmsg['note'], returnmsg['createtime'])
			print(logstr)
		else:
			return returnmsg

if __name__ == '__main__':
	itchat.auto_login(True)
	itchat.run()
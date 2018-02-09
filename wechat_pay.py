import itchat
import re
import time
import datetime

class wechat_pay():

	def __init__(self):
		self.printlog = False
		itchat.auto_login()

	def run(self):
		itchat.run()

	@itchat.msg_register(itchat.content.SHARING)
	def text_reply(msg):
		returnmsg = {}
		returnmsg['content'] = msg.Content

		try:
			returnmsg['fromuser'] = msg.fromUserName
			returnmsg['note'] = re.findall(re.compile(r'付款方备注：(.*?)\n'), content)[0]
			returnmsg['money'] = re.findall(re.compile(r'微信支付收款(.*?)元'), content)[0]
			returnmsg['createtime'] = datetime.datetime.utcnow()
		except IndexError:
			pass

		if returnmsg.note and returnmsg.money:
			if printlog:
				return printlog(returnmsg)
			else:
				return returnmsg
		else:
			return null

	def printlog(self, returnmsg):
		logstr = "From:%s, Money:%s, Note:%s, Time:%s" % (returnmsg.fromuser, returnmsg.money, returnmsg.note, returnmsg.createtime)
		print(logstr)


if __name__ == '__main__':
	wechat_pay = wechat_pay()
	wechat_pay.run()
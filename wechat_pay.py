import itchat
import re
import time
import datetime

@itchat.msg_register(itchat.content.SHARING)
def text_reply(msg):
	returnmsg = {}
	returnmsg['content'] = msg.Content

	try:
		returnmsg['fromuser'] = msg.fromUserName
		returnmsg['note'] = re.findall(re.compile(r'付款方备注：(.*?)\n'), returnmsg['content'])[0]
		returnmsg['money'] = re.findall(re.compile(r'微信支付收款(.*?)元'), returnmsg['content'])[0]
		returnmsg['createtime'] = datetime.datetime.utcnow()
	except IndexError:
		pass

	if returnmsg['note'] and returnmsg['money']:
		if printlog:
			logstr = "From:%s, Money:%s, Note:%s, Time:%s" % (returnmsg.fromuser, returnmsg.money, returnmsg.note, returnmsg.createtime)
			print(logstr)
		else:
			return returnmsg
	else:
		return null

if __name__ == '__main__':
	itchat.auto_login()
	itchat.run()
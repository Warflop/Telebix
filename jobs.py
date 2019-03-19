from telegram.ext import *
from PyQt4 import QtCore, QtGui
from pyzabbix import ZabbixAPI
from do_graph import *
import ConfigParser
import requests
import design
import time
import sys
import os

class App(QtGui.QMainWindow, design.Ui_Telebix):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

    def set_conf(self, section, id, value):

        config = ConfigParser.ConfigParser()
        config.read('resources/settings.ini')
        config.set(section,id,value)

        with open('resources/settings.ini', 'wb') as configfile:
            config.write(configfile)

    def init_button(self):

        self.stop_button.setEnabled(False)
        self.status.setStyleSheet("color: rgb(238, 82, 83)")
        self.status.setText("Not Running")
        self.start_button.clicked.connect(lambda: self.start_bot())
        self.stop_button.clicked.connect(lambda: self.stop_bot())
        self.get_id.clicked.connect(lambda: self.get_telegram_id())
        self.save_telegram.clicked.connect(lambda: self.set_telegram())
        self.save_zabbix.clicked.connect(lambda: self.set_zabbix())

    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(App, self).setVisible(visible)

    def plot_conf(self):

        config = ConfigParser.ConfigParser()
        config.read('resources/settings.ini')
        bot_token = config.get('Telegram','bot_token')
        t_user_id = config.get('Telegram','t_user_id')
        z_username = config.get('Zabbix','zabbix_user')
        z_password = config.get('Zabbix','zabbix_pass')
        z_host = config.get('Zabbix','zabbix_host')
        self.user_id.setText(str(t_user_id))
        self.bot_token.setText(str(bot_token))
        self.zabbix_host.setText(str(z_host))
        self.zabbix_user.setText(str(z_username))
        self.zabbix_pass.setText(str(z_password))

    def get_conf(self):

        config = ConfigParser.ConfigParser()
        config.read('resources/settings.ini')
        bot_token = config.get('Telegram','bot_token')
        t_user_id = config.get('Telegram','t_user_id')
        z_username = config.get('Zabbix','zabbix_user')
        z_password = config.get('Zabbix','zabbix_pass')
        z_host = config.get('Zabbix','zabbix_host')

        return str(bot_token), str(t_user_id), str(z_username), str(z_password), str(z_host)

    def get_telegram_id(self):

        try:
            requisicao = requests.get("https://api.telegram.org/bot" + self.bot_token.text() + "/getUpdates")
            if requisicao.json()['result'] != []:
                t_user_id = requisicao.json()['result'][0]['message']['from']['id']
                self.user_id.setText(str(t_user_id))
            else:
                self.user_id.setText("Talk with bot!")
        except:

            self.connect_test_telegram.setStyleSheet("color: rgb(238, 82, 83)")
            self.connect_test_telegram.setText("Invalid Token")

    def set_telegram(self):

        code = requests.get("https://api.telegram.org/bot" + self.bot_token.text() + "/getUpdates")

        try:

            if code.json()['result'] or code.json()['ok'] == True:
              
                self.set_conf('Telegram', 'bot_token', self.bot_token.text())
                self.set_conf('Telegram', 't_user_id', self.user_id.text())
                self.connect_test_telegram.setStyleSheet("color: rgb(16, 172, 132)")
                self.connect_test_telegram.setText("OK")

        except:

            self.connect_test_telegram.setStyleSheet("color: rgb(238, 82, 83)")
            self.connect_test_telegram.setText("Invalid Token")

    def set_zabbix(self):

        zabbix_host_text = self.zabbix_host.text()
        zabbix_user_text = self.zabbix_user.text()
        zabbix_pass_text = self.zabbix_pass.text()

        try:

            zapi = ZabbixAPI(str(zabbix_host_text))
            zapi.login(str(zabbix_user_text), str(zabbix_pass_text))
            self.connect_test.setStyleSheet("color: rgb(16, 172, 132)")
            self.connect_test.setText("OK")
            self.set_conf('Zabbix', 'zabbix_host', zabbix_host_text)
            self.set_conf('Zabbix', 'zabbix_user', zabbix_user_text)
            self.set_conf('Zabbix', 'zabbix_pass', zabbix_pass_text)

        except:

            self.connect_test.setStyleSheet("color: rgb(238, 82, 83)")
            self.connect_test.setText("Invalid Credentials")


    def start_bot(self):

        self.token, self.user_id_telegram, self.z_username, self.z_password, self.z_host = self.get_conf()
        self.zapi = ZabbixAPI(str(self.z_host))
        self.zapi.timeout = 4.0
        try:
            self.zapi.login(str(self.z_username), str(self.z_password))
        except:
            QtGui.QMessageBox.information(self, "Message", "Zabbix is not running! You need to fill in the connection details!")
            return

        self.updater = Updater(self.token)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler("hosts", self.info_hosts))
        dp.add_handler(CommandHandler("graphs", self.info_graphs, pass_args=True))
        dp.add_handler(CommandHandler("status", self.info_zabbix))
        dp.add_handler(CommandHandler("events", self.info_events))
        dp.add_handler(CommandHandler("webs", self.info_webs))
        dp.add_handler(CommandHandler("users", self.info_users))
        dp.add_handler(MessageHandler(Filters.text, self.echo))

        if self.infonotifications.isChecked():

            try:
                self.delete_script()
            except:
                pass

            try:
                self.create_script()
            except:
                QtGui.QMessageBox.information(self, "Message", "Check connection details!")
                return
        else:
            QtGui.QMessageBox.information(self, "Message", "You need to mark 'Realtime notification'!")
            return

        self.updater.start_polling()
        self.status.setStyleSheet("color: rgb(16, 172, 132)")
        self.status.setText("Running")      
        self.infohosts.setEnabled(False)
        self.infographs.setEnabled(False)
        self.infozabbix.setEnabled(False)
        self.infoevents.setEnabled(False)
        self.infowebs.setEnabled(False)
        self.infousers.setEnabled(False)
        self.infonotifications.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_bot(self):

        try:
            self.delete_script()
        except:
            pass

        self.updater.stop()
        self.status.setStyleSheet("color: rgb(238, 82, 83)")
        self.status.setText("Not Running")
        self.infohosts.setEnabled(True)
        self.infographs.setEnabled(True)
        self.infozabbix.setEnabled(True)
        self.infoevents.setEnabled(True)
        self.infowebs.setEnabled(True)
        self.infousers.setEnabled(True)
        self.infonotifications.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def help(self, bot, update):
        if str(update.message.chat_id) == self.user_id_telegram:
            update.message.reply_text("Welcome to Telebix!\n\nCommands available:\n<b>[+] /graphs hostname</b> - List images graphs of specific host\n<b>[+] /webs</b> - List monitored web scenarios\n<b>[+] /status</b> - List status of zabbix\n<b>[+] /events</b> - List last five events\n<b>[+] /help</b> - Help and information\n<b>[+] /hosts</b> - List hosts\n<b>[+] /users</b> - List users\n\nRead more on Github:\nhttps://github.com/Warflop/Telebix", parse_mode="HTML")
        else:
            update.message.reply_text("You shall not pass!")

    def echo(self, bot, update):
        if str(update.message.chat_id) == self.user_id_telegram:
            update.message.reply_text("Send <b>/help</b> to more information",parse_mode="HTML")
        else:
            update.message.reply_text("I can't give this information for you!")

    def info_hosts(self, bot, update):
        if str(update.message.chat_id) == self.user_id_telegram and self.infohosts.isChecked():
            for host in self.zapi.host.get(output="extend"):
                
                if int(host['status']) == 0:
                    self.hoststatus = "Enabled"
                else:
                    self.hoststatus = "Disabled"

                if (int(host['available']) == 1 or int(host['jmx_available']) == 1 or int(host['snmp_available']) == 1 or int(host['ipmi_available']) == 1):
                    update.message.reply_text("ID: {0} \nHost: {1} \nName: {2}\nStatus: {3}\n[Available]".format(host['hostid'],host['host'],host['name'],self.hoststatus))
                else:
                    update.message.reply_text("ID: {0} \nHost: {1} \nName: {2}\nStatus: {3}\n[Unavailable]".format(host['hostid'],host['host'],host['name'],self.hoststatus))
        else:
            update.message.reply_text("I can't give this information for you!")

    def info_graphs(self, bot, update, args):
        if str(update.message.chat_id) == self.user_id_telegram and self.infographs.isChecked():
            if args:
                str1 = ' '.join(args)
                check = self.zapi.graph.get(filter={"host":str(str1)})
                if check:

                    self.activehost = self.zapi.host.get(filter={"host":str(str1)})

                    if ((self.activehost[0]['status'] == '0') and (self.activehost[0]['available'] == '1' or self.activehost[0]['jmx_available'] == '1' or self.activehost[0]['snmp_available'] == '1' or self.activehost[0]['ipmi_available'] == '1')):

                        for graph in check:
                            if graph:
                                photo_graph = self.get_graph(graph['graphid'])
                                update.message.reply_photo(photo=open("/tmp/{0}.png".format(graph['graphid']), 'rb'), caption="Look, it's your {0} graph!".format(graph['name']))
                                os.remove("/tmp/{0}.png".format(graph['graphid']))
                    else:

                        update.message.reply_text("The host is disabled or unavailability.")

                else:
                    update.message.reply_text("There's no host with that name.")
            else:
                update.message.reply_text("Pass the hostname.")
        else:
            update.message.reply_text("I can't give this information for you!")
                    
    def info_zabbix(self, bot, update):
        if str(update.message.chat_id) == self.user_id_telegram and self.infozabbix.isChecked():
            try:
                self.zapi = ZabbixAPI(str(self.z_host))
                self.zapi.timeout = 4.0
                self.zapi.login(str(self.z_username), str(self.z_password))
                update.message.reply_text("Zabbix is running.")
            except:
                update.message.reply_text("Zabbix is not running.")
        else:
            update.message.reply_text("I can't give this information for you!")

    def info_events(self, bot, update):

        if str(update.message.chat_id) == self.user_id_telegram and self.infoevents.isChecked():

            for alert in self.zapi.trigger.get(output='extend',sortfield='triggerid',sortorder='DESC',only_true=1,active=1,expandDescription=True,selectHosts=["host"],limit=5):
                host = alert['hosts'][0]['host']
                priority = self.def_priority(int(alert['priority']))
                last_change = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(alert["lastchange"])))
                update.message.reply_text("[Alert]\nHost: {0}\nUrl: {1}\nPriority: {2}\nDescription: {3}\nLast Change: {4}"
                    .format(host,alert['url'],priority,alert['description'],last_change))

        else:
            update.message.reply_text("I can't give this information for you!")            

    def info_webs(self, bot, update):

        if str(update.message.chat_id) == self.user_id_telegram and self.infowebs.isChecked():
            for web in zapi.httptest.get(output='extend',monitored=True,selectSteps="extend"):
                for site in web['steps']:
                    update.message.reply_text("URL: {0} \nStatus code: {1}".format(site['url'],site['status_codes']))
        else:
            update.message.reply_text("I can't give this information for you!")

    def info_users(self, bot, update):
        if str(update.message.chat_id) == self.user_id_telegram and self.infousers.isChecked():
            for user in self.zapi.user.get(output='extend'):
                update.message.reply_text("ID: {0} \nUsername: {1} \nName: {2} {3}".format(user['userid'],user['alias'],user['name'],user['surname']))
        else:
            update.message.reply_text("I can't give this information for you!")

    def get_graph(self, zbx_graphid):

        tmp_dir = '/tmp/'

        zbx = ZabbixAPIGraph(server=str(self.z_host), username=str(self.z_username),
                        password=str(self.z_password))
        
        zbx.login()
        
        zbx_file_img = zbx.do_graph(zbx_graphid, tmp_dir)


        return zbx_file_img

    def def_priority(self,value):

        if value == 0:
            return "Not Classified"
        if value == 1:
            return "Information"
        if value == 2:
            return "Warning"
        if value == 3:
            return "Average"
        if value == 4:
            return "High"
        if value == 5:
            return "Disaster"

    def create_script(self):
        
        self.script = self.zapi.script.create({"name":"Telegram Script","command":"cd $(cut -d : -f 6 /etc/passwd | grep $(whoami))\necho 'BOT_TOKEN=$1\nMESSAGE=$3\ncurl -X POST --data \"parse_mode=MARKDOWN\" --data \"chat_id=$2\" --data \"text=$MESSAGE\" \"https://api.telegram.org/bot${BOT_TOKEN}/sendMessage\" > /dev/null' > telegram.sh","host_access":"3"})
        self.permission = self.zapi.script.create({"name":"Permission Script","command":"chmod +x /home/$(whoami)/telegram.sh","host_access":"3"})
        self.host = self.zapi.host.get(output="hostid")
        self.id_host = self.host[0]['hostid']
        self.id_script = self.script['scriptids'][0]
        self.id_permission = self.permission['scriptids'][0]

        self.zapi.script.execute(scriptid=int(self.id_script),hostid=int(self.id_host))
        self.zapi.script.execute(scriptid=int(self.id_permission),hostid=int(self.id_host))
        self.zapi.script.delete(int(self.id_script))
        self.zapi.script.delete(int(self.id_permission))

        self.action = self.zapi.action.create({'status' : 0,'name':'telegram_send','esc_period':60,'eventsource':0,'filter':{'evaltype':0,'conditions':[{'conditiontype':16,'operator':7,'value':''},{'conditiontype':5,'operator':0,'value':1}]},'operations':[{'operationtype':1,'esc_period':0,'evaltype':0,'opcommand_grp':[],'opconditions':[],'opcommand_hst':[{'hostid':0}],'esc_step_to':1,'esc_step_from':1,'opcommand': {'type':0,'command':'cd $(cut -d : -f 6 /etc/passwd | grep $(whoami)) | ./telegram.sh '+self.token + ' '+ self.user_id_telegram+' "*[{HOST.NAME} - {TRIGGER.STATUS}]*\n{TRIGGER.NAME}\nSeverity: {TRIGGER.SEVERITY}\nIP: {HOST.IP}\nDate: {DATE}"','execute_on':1}}]})

    def delete_script(self):

        self.id_action = self.zapi.action.get(filter={"name":"telegram_send"},output="actionid")
        self.zapi.action.delete(int(self.id_action[0]['actionid']))

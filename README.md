# Telebix
Telebix is an application that communicates with a Bot on the Telegram to receive commands and send information from an infrastructure monitored by Zabbix, which also sends messages in real time if any problems occur in the infrastructure, it is totally written in Python with Shell Script and has a graphical interface to help the network administrator more intuitively. The application can run on any computer as long as all credentials are properly posted.

<p align="center">
  <img align="center" src="https://i.imgur.com/obxCPTS.png" width="600">
</p>

# How to use

<h3>Creating a bot</h3>

<p align="center">
  <img align="center" src="https://i.imgur.com/VE6ZMjA.png" width="400">
</p>

<pre>
In the search bar on Telegram, type "BotFather" and send the command "/newbot".

The BotFather will ask for a name for your bot, after it will ask for a username as well.

Copy the generated access Token.

Send any message to your bot by Telegram.
</pre>

<h3>Installation</h3>

<iframe src="https://player.vimeo.com/video/296483913" width="640" height="402" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

<pre>
git clone https://github.com/Warflop/Telebix.git
cd Telebix
chmod +x setup.sh
sudo ./setup.sh --install
</pre>

<h3>Configuration</h3>

<p align="center">
  <img align="center" src="https://i.imgur.com/br0tmrx.png" width="300">
</p>

<pre>
In the Settings tab are the fields to be populated with the Zabbix login information, bot token and Telegram user ID (or Group ID).

The token you already have after creating the Bot. 

To get the user ID you can use the "GET ID" button in the settings tab after talking to the bot or add manually,
access the address below by changing <b>TOKENHERE</b> by the token you copied, there will be your user ID.

You can use the ID of any group that you are entered as well.

https://api.telegram.org/bot<b>TOKENHERE</b>/getUpdates
</pre>

<p align="center">
  <img align="center" src="https://i.imgur.com/wNabrKe.png" width="550">
</p>

# Commands Available

<p align="center">
  <img align="center" src="https://i.imgur.com/ZgXWGn9.png" width="550">
</p>

<pre>
<b>[+] /graphs hostname </b>- List images graphs of specific host
<b>[+] /webs </b>- List monitored web scenarios
<b>[+] /status </b>- List status of zabbix
<b>[+] /events </b>- List last five events
<b>[+] /help </b>- Help and information
<b>[+] /hosts </b>- List hosts
<b>[+] /users </b>- List users
</pre>

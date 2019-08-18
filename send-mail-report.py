#!/usr/bin/env python

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

senderEmail = "$SRC_EMAIL"
password = "$PASSWD_SRC_EMAIL"
receiverEmail = "$DEST_EMAIL"

msg = MIMEMultipart()
msg['Subject'] = "Analise SquidAnalyzer"
msg['From'] = senderEmail
msg['To'] = receiverEmail

body = """\
Analise Concluida com Sucesso!!!




"""
htmlTop = """\
<html>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8" />
<style type="text/css"><!--

html, body { margin:0; padding: 0; height: 100%; font-family: "Trebuchet MS", Verdana, Arial, Helvetica; }
body { font-size: 10pt; background-color: #F1F1F1; min-width: 900px; }
h1 { font-family: "Trebuchet MS", Verdana, Arial, Helvetica; color: #76add2; }
h2 { font-style: italic; font-family: "Trebuchet MS", Verdana, Arial, Helvetica; color: #76add2; }
.notification { color: #222222; font-style: italic; font-size:0.8em; }
#conteneur { height: auto !important; min-height: 100%; height: 100%; position: relative; }
.line-separator { height:1px; width:520px; background:#717171; border-bottom:1px solid #313030; margin-top:-25px; margin-left: 10px; margin-bottom: 45px; }
.descLegend { font-style: italic; }
.legendeTitle { font-variant: small-caps; font-weight: bold; font-size: 1.3em; line-height: 18pt; letter-spacing: 2px; }
#alignLeft { float: left; }
.italicPercent { font-style: italic; font-size: 0.7em; }
#contenu { padding-bottom: 50px; }
#contenu h4 { font-size: 1.6em; font-variant: small-caps; padding-left: 15px; letter-spacing: 2px; }
#contenu h3 { font-size: 1.2em; font-variant: small-caps; padding-left: 15px; letter-spacing: 2px; }
.displayGraph { border: 0px; }
div.uplink { margin-top: 30px; margin-left: 0; margin-right: 0; text-align: center; }
div.uplink a { color: #222222; text-decoration: none; font-variant: small-caps; font-weight: bold; }
div.uplink a:hover { color: #76add2; }
table.stata td a.domainLink { font-size: 0.9em; font-variant: normal; font-style: italic; }
table.graphs { margin-right: auto; margin-left: auto; }
table.stata th.headerBlack { color: #222222; font: bold 15px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif; font-variant: small-caps; }
table.stata { border-collapse: collapse; width: 90%; margin-left:auto; margin-right:auto; border: 0px; white-space:nowrap; }
table.stata th { background: #76add2; font: 12px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif; font-variant: small-caps; letter-spacing: 2px; padding-left: 20px; padding-right: 20px; padding-top: 3px; padding-bottom: 3px; border: 2px solid silver; color: #F1F1F1; }
table.stata td { text-align: center; padding-left: 20px; padding-right: 20px; padding-top: 5px; padding-bottom: 5px; border: 2px solid silver; font-style: italic; }
table.stata th.nobg { background: none; border-top: 0px; border-left: 0px; padding-left: 20px; padding-right: 20px; padding-top: 3px; padding-bottom: 3px; }
table.stata td a { font-variant: small-caps; text-decoration: none; color: #222222; font-weight: bold; font-style: normal; font-size: 14px; }
table.stata td a:hover { color: #76add2; }
.displayLegend { margin-left: 150px; }
.iconUpArrow { background-image: url("./images/up-arrow.png"); background-position: left bottom; background-repeat: no-repeat; padding-left: 25px; margin-bottom: 20px; }

--></style>
	<body>
		<h1>Squid-Analyzer Report</h1>
		<h2>Top-10 Users</h2><br>
		<div>
			<table class="sortable stata">
				<thead>
					<tr>
						<th>Login</th>
						<th>Users</th>
						<th>Requests (%)</th>
						<th>Bytes (%)</th>
						<th>Duration (%)</th>
						<th>Throughput (Bytes/s)</th>
						<th>Largest</th>
						<th style="text-align: left;">Url</th>
					</tr>
				</thead>
				<tbody>
"""
htmlBottom = """\
				</tbody>
        	        </table>
		</div>
        </body>
</html>

"""

arq = open('/var/www/squidanalyzer/2019/user.html', 'r')
htmlCode = arq.readlines()
arq.close()

users = []
codeLine = []
gravar = 0
i = 0

for line in htmlCode:
  if (line == '<tr>\n' and htmlCode[i - 1] != '<thead>\n'):
    gravar = 1

  if (gravar == 1):
    codeLine.append(line)
  else:
    codeLine = []

  if (line == '</tr>\n' and gravar == 1):
    gravar = 0
    users.append(codeLine)

  i += 1

for i in range(len(users)):
  for j in range(i, len(users)):
    if (int(users[i][4].split(">")[1].split()[0].replace(',', '')) < int(users[j][4].split(">")[1].split()[0].replace(",", ""))):
      aux = users[i]
      users[i] = users[j]
      users[j] = aux

html = htmlTop

for i in range(0, 10):
  for j in range(len(users[i])):
    html += users[i][j]

html += htmlBottom

msg.attach(MIMEText(html.decode('utf-8'), 'html', 'utf-8'))

server = smtplib.SMTP("$SERVER_ADDRESS", $PORT)
server.starttls()
server.login(msg['From'], password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()


import re

html = '''<html>
<head><title>Kyra - created with Hero Lab&reg;</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
</head>
<body>
<b>Kyra</b><br/>
Female Human Cleric 1<br/>
NG Medium humanoid (human)<br/>
<b>Init </b>+0; <b>Senses </b>Perception +3<br/>
</body>
</html>
'''



html = re.sub(r"\<meta http-equiv.*?\>", '', html)

print html

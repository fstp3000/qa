import requests
#from bs4 import BeautifulSoup
import json

url_list=['https://docs.google.com/forms/d/1xPSu0lT2Mr1XGSpVRlvk6DNQbeEySLOn3Kuxq0S-pv4/viewform?fbclid=IwAR3fUuFlZWmCWq1s7jVGLj6VSvSV3pp00_DtGRTc1_xXFFEW9xL7EqSKHQM&edit_requested=true#responses',
	'https://docs.google.com/forms/d/e/1FAIpQLSfKeNxWwzaEBEykLBivIBjkEZEbnJPaB65C-psY2CaVicrReA/viewform',
	'https://docs.google.com/forms/d/e/1FAIpQLSeytV2CVM_vPYl3kGhG_ZGC1ybYjKaUt-r_EVyVvjZJecZwEQ/viewform?usp=send_for'
	]

for url in url_list:
	res = requests.get(url).text
	start = res.find('FB_PUBLIC_LOAD_DATA_')
	end = res.find('</script>', start)
	res = res[start+23:end-1]
	#print(res)
	res = json.loads(res)[1]
	print('topic\n',res[0])
	print('#####################################')
	res = res[1]
	for i in res:
		print(i)
		print('--------------------------------------------------------------------------------------------')
	print('=================================================================================================')
	print('=================================================================================================')
	print('=================================================================================================')

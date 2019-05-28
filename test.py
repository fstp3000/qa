import requests
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
	res = json.loads(res)[1]
	#print('topic\n',res[0].replace(" ",""))
	res = res[1]
	count = 0
	for i in res:
		if i[-1] == 6:
			if count == 0:
				count = 1
				print('topic')
				print(i[1])
				print('content')
				if (i[2]==None):
					print("No content")
				else:
					print(i[2].replace(" ",""))
				print('###########################################################################################')
			else:
				break
		elif i[3] == 2 or i[3]==4 or i[3] == 5:
			print('Question:',i[1])
			print('Answers:')
			for answer in i[4][0][1]:
				print(answer[0])
			#print('answer',i[4][0][1])
			print('--------------------------------------------------------------------------------------------')
		elif i[3] == 8:
			print('group question name:', i[1])
			print('********************************************************************************************')
		elif i[3] == 0:
			next
		else:
			print(i)
			print('--------------------------------------------------------------------------------------------')
	print('=================================================================================================')
	print('=================================================================================================')
	print('=================================================================================================')

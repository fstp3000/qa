import requests
import json

url_list=['https://docs.google.com/forms/d/1xPSu0lT2Mr1XGSpVRlvk6DNQbeEySLOn3Kuxq0S-pv4/viewform?fbclid=IwAR3fUuFlZWmCWq1s7jVGLj6VSvSV3pp00_DtGRTc1_xXFFEW9xL7EqSKHQM&edit_requested=true#responses',
	'https://docs.google.com/forms/d/e/1FAIpQLSfKeNxWwzaEBEykLBivIBjkEZEbnJPaB65C-psY2CaVicrReA/viewform',
	'https://docs.google.com/forms/d/e/1FAIpQLSeytV2CVM_vPYl3kGhG_ZGC1ybYjKaUt-r_EVyVvjZJecZwEQ/viewform?usp=send_for'
	]

for url in url_list:
	res = requests.get(url).text
	topic_start = res.find('<meta itemprop="name" content="')
	topic_end = res.find('">', topic_start)
	start = res.find('FB_PUBLIC_LOAD_DATA_')
	end = res.find('</script>', start)
	#####
	title = res[topic_start+31: topic_end]
	#####
	res = res[start+23:end-1]
	res = json.loads(res)[1]
	print('title:',title)
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
					print(i[2].replace("	",""))
				print('#############################################')
			else:
				break
		elif i[3] == 2 or i[3]==4 or i[3] == 5:
			print('Question:',i[1])
			print('Answers:')
			for index,answer in enumerate(i[4][0][1]):
                                if answer[0]=="":
                                    break
                                print(index,end='')
                                print(':',end='')
                                print(answer[0],end='')
                                print('  ',end='')
			#print('answer',i[4][0][1])
			print('\n-----------------------------------------------------')
		elif i[3] == 8:
			print('group question name:', i[1])
			print('*****************************************************')
		elif i[3] == 0 or i[3] == 1:
			next
		else:
			#assert (i[3] != 11)
			print(i)
			print('-----------------------------------------------------')
	print('=====================================================================')
	print('=====================================================================')
	print('=====================================================================')

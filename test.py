#coding=utf-8
import requests
import json
import pprint
url_list=['https://docs.google.com/forms/d/1xPSu0lT2Mr1XGSpVRlvk6DNQbeEySLOn3Kuxq0S-pv4/viewform?fbclid=IwAR3fUuFlZWmCWq1s7jVGLj6VSvSV3pp00_DtGRTc1_xXFFEW9xL7EqSKHQM&edit_requested=true#responses',
	'https://docs.google.com/forms/d/e/1FAIpQLSfKeNxWwzaEBEykLBivIBjkEZEbnJPaB65C-psY2CaVicrReA/viewform',
	]

for url in url_list:
    data={"題目":"None","標題":"未命名的標題","標題描述": "無描述"}
    res = requests.get(url).text
    topic_start = res.find('<meta itemprop="name" content="')
    topic_end = res.find('">', topic_start)
    start = res.find('FB_PUBLIC_LOAD_DATA_')
    end = res.find('</script>', start)
    #####
    title = res[topic_start+31: topic_end]
    #####
    res = res[start+23:end-1]
    #print(res)
    res = json.loads(res)[1]
    data['題目']=title
    print('title:',title)
    res = res[1]
    count = 0
    set_qa=[]
    group_qa = {"題組名稱":"None"}
    qas = {}
    for i in res:
        if i[-1] == 6:
            if count == 0:
                count = 1
                print('標題')
                print(i[1])
                data['標題']=i[1]
                print('標題描述')
                if (i[2]==None):
                    print("No content")
                else:
                    data['標題描述']=i[2]
                    print(i[2].replace(" ",""))
                    print('#############################################')
            else:
                break
        elif i[3] == 2 or i[3]==4 or i[3] == 5:
            question=i[1][i[1].find('.')+1:]
            print('Question:',question)
            print('Answers:')
            uni_ans=[]
            ans={}
            for index,answer in enumerate(i[4][0][1]):
                if answer[0]=="":
                    break
                print(index,end='')
                print(':',end='')
                print(answer[0],end='')
                print('  ',end='')
		#print('answer',i[4][0][1])
                uni_ans.append(answer[0])
            ans["可選答案"]=uni_ans
            ans["答案"]="None"
            qas[question]=ans
            print('\n-----------------------------------------------------')
        elif i[3] == 8:
            group_qa['問題']=qas
            set_qa.append(group_qa)
            qas={}
            group_qa = {}
            print('group question name:', i[1])
            print('*****************************************************')
        elif i[3] == 0 or i[3] == 1:
            next
        else:
            #assert (i[3] != 11)
            print(i)
            print('-----------------------------------------------------')
    data["題組"]=set_qa
    print(data)
    with open(title+'.json', 'w') as outfile:
        json.dump(data, outfile)
    print('=====================================================================')
    print('=====================================================================')
    print('=====================================================================')

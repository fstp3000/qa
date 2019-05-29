#coding=utf-8
import requests
import json
import pprint
url_list=[
    #'https://docs.google.com/forms/d/1xPSu0lT2Mr1XGSpVRlvk6DNQbeEySLOn3Kuxq0S-pv4/viewform?fbclid=IwAR3fUuFlZWmCWq1s7jVGLj6VSvSV3pp00_DtGRTc1_xXFFEW9xL7EqSKHQM&edit_requested=true#responses',
#	'https://docs.google.com/forms/d/e/1FAIpQLSfKeNxWwzaEBEykLBivIBjkEZEbnJPaB65C-psY2CaVicrReA/viewform',
#	'https://docs.google.com/forms/d/e/1FAIpQLSfKeNxWwzaEBEykLBivIBjkEZEbnJPaB65C-psY2CaVicrReA/viewform',
  #        'https://docs.google.com/forms/d/1xPSu0lT2Mr1XGSpVRlvk6DNQbeEySLOn3Kuxq0S-pv4/viewform?fbclid=IwAR3fUuFlZWmCWq1s7jVGLj6VSvSV3pp00_DtGRTc1_xXFFEW9xL7EqSKHQM&edit_requested=true#responses',
 #'https://docs.google.com/forms/d/e/1FAIpQLSdQICeYZ30apILh2VknzPqemIkzjb2kp_bv1LlVDUIRCMUUDg/viewform',
#          'https://docs.google.com/forms/d/e/1FAIpQLSeOkfOimyjzjQ_wHUb6GDVxv9NlzhBZPKxRHlFeJBe1iIGGgQ/viewform?fbclid=IwAR2qvgvotRONvox_9MNls_H5Fy2n8Q8P33HnphUUzd2DsLp4A-BgZtMROok',
          'https://docs.google.com/forms/d/e/1FAIpQLSf7mx78hpk8BfDi_nrBeZ9uwynDC1RdIUzcymIoNXeyEiEVsA/viewform'
         # 'https://docs.google.com/forms/d/e/1FAIpQLSfxZy5eNrgSJouLEti48QgpJnnh4eDs7m13H6gV1y_9g1fBEQ/viewform',
         # 'https://docs.google.com/forms/d/e/1FAIpQLScwnJzVG25ZkHd03NPGyHyqx_FBxyYXJLNR4KSti817lmvUQQ/viewform',
         # 'https://docs.google.com/forms/d/e/1FAIpQLSfqSBIUbn-1OX3ErlNvyBkNnckj0nmo-waBPSoTcKJqBvMAoQ/viewform',
         # 'https://docs.google.com/forms/d/e/1FAIpQLSep4L-pfPppimxr2pS6QxSftitIa3FPCfKrXqKJyQ3ZDZmPtQ/viewform'
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
    data['題目']=title.replace('\t',"").replace('\n',"")
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
                    data['標題描述']=i[2].replace('\t',"").replace('\n',"")
                    print(i[2].replace(" ",""))
                    print('#############################################')
            else:
                break
        elif i[3] == 2 or i[3]==4 or i[3] == 5:
            if type(i[1]) == None:
                next
            try:
                point = i[1].find('.')
            except AttributeError:
                print(i[1])
            if point != -1:
                question=i[1][i[1].find('.')+1:].replace('\t',"").replace('\n',"")
            else:
                question=i[1].replace('\t',"").replace('\n',"")
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
            id = 0
            if qas != {}:
                for key, _ in qas.items():
                    if "性別" in key or "年齡" in key or "職業" in key:
                        id += 1
                    if id> 2:
                        data["個資"]= qas
                    else:
                        group_qa['問題']=qas
                set_qa.append(group_qa)
                qas={}
                group_qa = {"題組名稱":i[1]}
                print('group question name:', i[1])
                print('*****************************************************')
            else:
                qas={}
                group_qa = {"題組名稱":i[1]}
        elif i[3] == 0 or i[3] == 1:
            next
        else:
            #assert (i[3] != 11)
            print(i)
            print('-----------------------------------------------------')
    data["題組"]=set_qa
    set_qa=[]
    print(data)
    with open(title+'.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    print('=====================================================================')
    print('=====================================================================')
    print('=====================================================================')

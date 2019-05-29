#coding=utf-8
import requests
import json
import csv
import pprint
with open('q.csv', newline='') as f:
    url_list = csv.reader(f, delimiter=',')
    url_list = list(url_list)
#url_list=[url_list[2]]
check_list = []
check = []
is_packqas = False
for url in url_list:
    check.append(url[0])
    data={"題目":"None","標題":"未命名的標題","標題描述": "無描述"}
    res = requests.get(url[1]).text
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
    data['題目']=title.replace('\t',"").replace('\n',"").replace(' ',"").replace('  ',"")
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
                    data['標題描述']=i[2].replace('\t',"").replace('\n',"").replace(' ',"").replace('  ',"")
                    print(i[2].replace(" ",""))
                    print('#############################################')
            else:
                break
        elif i[3] == 2 or i[3]==4 or i[3] == 5:
            if i[1] is None:
                continue
            try:
                point = i[1].find('.')
            except AttributeError:
                print(i[1])
            if point != -1:
                question=i[1][i[1].find('.')+1:].replace('\t',"").replace('\n',"").replace(' ',"").replace('  ',"")
            else:
                print(i[1])
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
            is_packqas=False
            print('\n-----------------------------------------------------')
        elif i[3] == 7:
            try:
                print(i)
                if i[4] is None:
                    continue
                try:
                    point = i[4][3][3][0].find('.')
                except AttributeError:
                    print(i[1])
                if point != -1:
                    question=i[4][3][3][0][i[4][3][3][0].find('.')+1:].replace('\t',"").replace('\n',"").replace(' ',"").replace('  ',"")
                else:
                    print(i[4][3][3][0])
                    question=i[4][3][3][0].replace('\t',"").replace('\n',"")
                print('Question:',question)
                print('Answers:')
                uni_ans=[]
                ans={}
                print(i[4][3][1])
                for index,answer in enumerate(i[4][3][1]):
                    #if answer[0]=="":
                    #    break
                    print(index,end='')
                    print(':',end='')
                    print(answer[0],end='')
                    print('  ',end='')
                    #print('answer',i[4][0][1])
                    uni_ans.append(answer[0])
                ans["可選答案"]=uni_ans
                ans["答案"]="None"
                qas[question]=ans
                is_packqas=False
                print('\n-----------------------------------------------------')
            except:
                continue
        elif i[3] == 8:
            id = 0
            if qas != {}:
                for key, _ in qas.items():
                    if "性別" in key or "年齡" in key or "職業" in key or "學歷" in key:
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
    if is_packqas==False:
        is_packqas=True
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

    if set_qa != []:
        data["題組"]=set_qa
        if "個資" not in data:
            data["個資"]={}
        set_qa=[]
        print(data)
        with open('./qa/'+title+'.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
        check.append('ok')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
    check_list.append(check)
    check = []
pprint.pprint(check_list)

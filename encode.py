import json
import os

path = './qa/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

for filename in files:
    #print(filename)
    with open(filename) as f:
        data = json.load(f)
        data = dict(data)
    el_tag = '[p_tag]'
    qa_tag = '[qa_tag]'
    id_tag = '[id_tag]'
    id_ans_tag = '[id_ans_tag]'

    topic = data['題目']
    title = data['標題']
    if title == None:
        title = "None"
    title_content = data['標題描述']
    iden = data['個資']
    qa_set = data['題組']
    #print(topic)
    #print(title)
    #print(title_content)
    #print(iden)
    out = el_tag + topic + el_tag + title + el_tag + title_content

    identity = ''
    if iden != {}:
        for characristic, answer in iden.items():
            identity = identity + id_tag + characristic + id_ans_tag + answer["答案"]
    for qa in qa_set:
        for question, answer in qa['問題'].items():
            print(out+ identity+ qa_tag+ question)
    print('======================================================')
    print('======================================================')
    print('======================================================')

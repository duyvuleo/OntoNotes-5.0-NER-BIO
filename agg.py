import os, glob, itertools
import sys

def generate_collection(tag="train", language='english', ext='gold_conll'):
    results = itertools.chain.from_iterable(glob.iglob(os.path.join(root,f'*.{ext}'))
                                               for root, dirs, files in os.walk(f'./conll-formatted-ontonotes-5.0/data/{tag}') if language in root)

    #print([os.path.join(root,'*.v9_gold_parse_conll') for root, dirs, files in os.walk(f'./conll-formatted-ontonotes-5.0/data/{tag}') if language in root])
 
    text =  ""
    for cur_file in results: 
        with open(cur_file, 'r') as f:
            print(cur_file)
            flag = None
            for line in f.readlines():
                l = line.strip()
                l = ' '.join(l.split())
                ls = l.split(" ")
                if len(ls) >= 11:
                    word = ls[3]
                    pos = ls[4]
                    cons = ls[5]
                    ori_ner = ls[10]
                    ner = ori_ner
                    # print(word, pos, cons, ner)
                    if ori_ner == "*":
                        if flag==None:
                            ner = "O"
                        else:
                            ner = "I-" + flag
                    elif ori_ner == "*)":
                        ner = "I-" + flag
                        flag = None
                    elif ori_ner.startswith("(") and ori_ner.endswith("*") and len(ori_ner)>2:
                        flag = ori_ner[1:-1]
                        ner = "B-" + flag
                    elif ori_ner.startswith("(") and ori_ner.endswith(")") and len(ori_ner)>2 and flag == None:
                        ner = "B-" + ori_ner[1:-1]

                    text += "\t".join([word, pos, cons, ner]) + '\n'
                else:
                    text += '\n'
            text += '\n'
            # break

    with open("onto."+tag+".ner."+language, 'w') as f:
        f.write(text)


generate_collection("train", sys.argv[1], 'v4_gold_conll')
generate_collection("test", sys.argv[1], 'v4_gold_conll')
generate_collection("development", sys.argv[1], 'v4_gold_conll')
generate_collection("conll-2012-test", sys.argv[1], 'v9_gold_parse_conll')


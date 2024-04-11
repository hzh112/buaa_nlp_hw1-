# 三元模型
import os
import re
from collections import Counter
def DFS_file_search(dict_name):
    # list.pop() list.append()这两个方法就可以实现栈维护功能
    stack = []
    result_txt = []
    stack.append(dict_name)
    while len(stack) != 0:  # 栈空代表所有目录均已完成访问
        temp_name = stack.pop()
        try:
            temp_name2 = os.listdir(temp_name)  # list ["","",...]
            for eve in temp_name2:
                stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
        except NotADirectoryError:
            result_txt.append(temp_name)
    return result_txt
# path_list = DFS_file_search(r"C:\Users\Acer\Desktop\Chinese corpus")
# path_list 为包含所有小说文件的路径列表
corpus = []

with open("C:\\Users\\Acer\\Desktop\\Chinese corpus\\4.txt", "r", encoding="utf-8") as file:
    text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
    corpus += text
# corpus 存储语料库，其中以每一个自然段为一个分割
regex_str = ".*?([^\u4E00-\u9FA5]).*?"
english = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;「<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
symbol = []
for j in range(len(corpus)):
    corpus[j] = re.sub(english, "", corpus[j])
    symbol += re.findall(regex_str, corpus[j])
count_ = Counter(symbol)
count_symbol = count_.most_common()
noise_symbol = []
for eve_tuple in count_symbol:
    if eve_tuple[1] < 200:
        noise_symbol.append(eve_tuple[0])
noise_number = 0
for line in corpus:
    for noise in noise_symbol:
        line.replace(noise, "")
        noise_number += 1
#三元模型
import jieba
from collections import Counter
import math
import re

def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# with open("C:\\Users\\Acer\\Desktop\\Chinese corpus\\1.txt", "r", encoding="utf-8") as f:
#     corpus = [eve.strip("\n") for eve in f]
# 3-gram
def combine3gram(cutword_list):
    if len(cutword_list) <= 2:
        return []
    res = []
    for i in range(len(cutword_list)-2):
        res.append(cutword_list[i] + cutword_list[i+1] + " " + cutword_list[i+2] )
    return res
token_3gram = []
result = []
for para in corpus:
    word = []
    for j in para:
        word += j
    result += jieba.lcut(para)
    # token += word
with open("C:\\Users\\Acer\\Desktop\\cn_stopwords.txt", encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
    con = f.readlines()
    stop_words = set()
    for i in con:
        i = i.replace("\n", "")  # 去掉读取每一行数据的\n
        stop_words.add(i)
for word in result:
    if word not in stop_words:
# for para in corpus:
    # cutword_list = [removePunctuation(eve) for eve in cutword_list if removePunctuation(eve) != ""]
        token_3gram += combine3gram(word)
# 3-gram的频率统计
token_3gram_num = len(token_3gram)
ct3 = Counter(token_3gram)
vocab3 = ct3.most_common()
# print(vocab3[:20])
# 3-gram相同句首两个词语的频率统计
same_2st_word = [eve.split(" ")[0] for eve in token_3gram]
assert token_3gram_num == len(same_2st_word)
ct_2st = Counter(same_2st_word)
vocab_2st = dict(ct_2st.most_common())
entropy_3gram = 0
for eve in vocab3:
    p_xyz = eve[1]/token_3gram_num
    first_2word = eve[0].split(" ")[0]
    entropy_3gram += -p_xyz*math.log(eve[1]/vocab_2st[first_2word], 2)
L = [[0]*2 for i in range(10)]
i = 0
j = 1
while True:
    L[i][0] = vocab3[j][0]
    L[i][1] = vocab3[j][1]
    L[i][0] = L[i][0].replace(' ', '')
    L[i][0] = remove_punctuation(L[i][0])
    if not is_contain_chinese(L[i][0]):
        j = j+1
        continue
    i = i+1
    j = j+1
    if i == 10:
        break
print("词库总词数：", token_3gram_num, " ", "不同词的个数：", len(vocab3))
print("出现频率前10的3-gram词语：", L)
print("entropy_3gram:", entropy_3gram)
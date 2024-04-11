# 二元分词
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

# 2-gram
def combine2gram(cutword_list):
    if len(cutword_list) == 1:
        return []
    res = []
    for i in range(len(cutword_list)-1):
        res.append(cutword_list[i] + " " + cutword_list[i+1])
    return res
token_2gram = []
corpus = []
with open("C:\\Users\\Acer\\Desktop\\Chinese corpus\\4.txt", "r", encoding="utf-8") as file:
    text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
    corpus += text
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
token = []
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
        # token_2gram.append(word)
        # print(word)
        token_2gram += combine2gram(word)
# print(token_2gram)
# 2-gram的频率统计
token_2gram_num = len(token_2gram)
ct2 = Counter(token_2gram)
vocab2 = ct2.most_common()
# print(vocab2[:20])
# 2-gram相同句首的频率统计
same_1st_word = [eve.split(" ")[0] for eve in token_2gram]
assert token_2gram_num == len(same_1st_word)
ct_1st = Counter(same_1st_word)
vocab_1st = dict(ct_1st.most_common())
entropy_2gram = 0

for eve in vocab2:
    p_xy = eve[1]/token_2gram_num
    first_word = eve[0].split(" ")[0]
    # p_y = eve[1]/vocab_1st[first_word]
    entropy_2gram += -p_xy*math.log(eve[1]/vocab_1st[first_word], 2)
L = [[0]*2 for i in range(10)]
i = 0
j = 1
while True:
    L[i][0] = vocab2[j][0]
    L[i][1] = vocab2[j][1]
    L[i][0] = L[i][0].replace(' ', '')
    L[i][0] = remove_punctuation(L[i][0])
    if not is_contain_chinese(L[i][0]):
        j = j+1
        continue
    i = i+1
    j = j+1
    if i == 10:
        break
print("词库总词数：", token_2gram_num, " ", "不同词的个数：", len(vocab2))
print("出现频率前10的2-gram词语：", L)
print("entropy_2gram:", entropy_2gram)
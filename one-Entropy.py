# 一元分词
import jieba
from collections import Counter
import math
import re

# 1-gram
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
# print(corpus)
token = []
result = []
for para in corpus:
    word = []
    for j in para:
        word += j
    result += jieba.lcut(para)
    # token += word
with open("C:\\Users\\Acer\\Desktop\\NLP_work1\\cn_stopwords.txt", encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
    con = f.readlines()
    stop_words = set()
    for i in con:
        i = i.replace("\n", "")  # 去掉读取每一行数据的\n
        stop_words.add(i)
for word in result:
    if word not in stop_words:
        token.append(word)
token_num = len(token)
ct = Counter(token)
vocab1 = ct.most_common()
entropy_1gram = sum([-(eve[1]/token_num)*math.log((eve[1]/token_num),2) for eve in vocab1])
print("词库总词数：", token_num, " ", "不同词的个数：", len(vocab1))
print("出现频率前10的1-gram词语：", vocab1[:10])
print("entropy_1gram:", entropy_1gram)
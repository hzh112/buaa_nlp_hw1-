import re
import collections
import matplotlib.pyplot as plt
import os

def show_Zipf(word_dict):
    '''
    将词频结果按着由高到低的顺序排列，然后绘制Zipf定律
    '''
    print('词频排列如下')
    freq = [v for v in sorted(word_dict.values(), reverse=True)]
    plt.rcParams['figure.figsize'] = (10.0, 8.0)
    plt.loglog(freq)  # 双对数坐标
    plt.title('frequency-rank')
    plt.xlabel('rank')
    plt.ylabel('word frequency')
    plt.show()


def count_pos(word_pos_list):
    '''
    统计词性的出现频次
    word_pos_list:列表，以词/词性组成的元组为元素
    ---
    返回词性频率字典：pos_dict
    '''
    word_dict = {}

    for i in word_pos_list:
        if not word_dict.get(i[0]):
            word_dict[i[0]] = 1
        else:
            word_dict[i[0]] += 1
    print('已分别建立词频词典，词性词频词典')
    return word_dict


def fenci_jieba(text):
    '''
    text,是上面程序生成的列表，元素是句子
    使用结巴分词，词性标注
    '''
    # 列表,以词/词性组成的元组为元素
    word_pos_list = []

    import jieba.posseg as pseg
    for line in text:
        if line:
            line = pseg.lcut(line)
            for word, flag in line:
                word_pos_list.append((word, flag))
    return word_pos_list

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

def file2sentences():
    # path_list = DFS_file_search(r"C:\Users\Acer\Desktop\NLP_work1\jyxstxtqj_downcc.com")
    # path_list 为包含所有小说文件的路径列表
    corpus = []

    with open("C:\\Users\\Acer\\Desktop\\Chinese corpus\\1.txt", "r", encoding="utf-8") as file:
        text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
        corpus += text
    # corpus 存储语料库，其中以每一个自然段为一个分割
    regex_str = ".*?([^\u4E00-\u9FA5]).*?"
    english = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;「<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    for j in range(len(corpus)):
        corpus[j] = re.sub(english, "", corpus[j])
    return corpus

def main1():
    text = file2sentences()
    word_pos_list = fenci_jieba(text)
    word_dict = count_pos(word_pos_list)
    show_Zipf(word_dict)

def show_Zipf2(word_dict):
    '''
    将词频结果按着由高到低的顺序排列，然后绘制Zipf定律
    '''
    print('词频—数量关系曲线（Zipf第二定律）', '\n')
    print('词频排列如下')
    word_freq = [v for v in sorted(word_dict.values(), reverse=True)]
    freq_num = sorted([sum([1 for w in word_freq if word_freq[w] == n]) for n in range(1, word_freq[0] + 1)],
                      reverse=True)
    print(freq_num)
    plt.loglog(range(1, word_freq[0] + 1), freq_num, '.')
    plt.title('frequency-number')
    plt.xlabel('rank')
    plt.ylabel('word frequency')
    plt.show()


main1()
#coding:utf-8
# 读取Mongo中短评数据，对其进行中文分词，并生成词云
# 读取Mongo中的短评数据
# https://pypi.org/project/pymongo/
# http://github.com/mongodb/mongo-python-driver

import pymongo
import jieba
from jieba import analyse
import collections
from matplotlib import pyplot
from wordcloud import WordCloud
from pyecharts import Bar
from pyecharts import Funnel

#生成词云
def countCiYun():
    text = None
    with pymongo.MongoClient(host='127.0.0.1', port=27017) as client:
        comments = client.qichezhijia.qichezhijia1
        print('数据总条数count:', comments.estimated_document_count())
        # pymongo.cursor.Cursor
        cursor = comments.find()
        # 遍历数据，这里只遍历短评数据(好在数据量并不太大)
        text = ''.join(map(lambda doc: doc.get('comment'), cursor))
    
    #用户自定义分词
    jieba.load_userdict(r'../analysis/user_dict.txt')
    #屏蔽关键词列表
    analyse.set_stop_words(r'../analysis/stopwords.txt')
    
    m=collections.Counter(text)
    tags = analyse.extract_tags(text, topK=30, withWeight=False)
    #词云所有词列表
    new_text = ' '.join(tags)
    countFinalWordsList(text,new_text)
    
    # 对分词文本生成词云
    # 生成词云，需要指定支持中文的字体，否则无法生成中文词云
    wc = WordCloud(
        max_words=200,   # 设置词云最大单词数
        width=1099, # 设置词云图片宽、高
        height=724,
        # 设置词云文字字体(美化和解决中文乱码问题)
        font_path=r'../example/fonts/FZXingKai-S04S.TTF').generate(new_text)
    
    # 绘图(标准长方形图)
    pyplot.imshow(wc, interpolation='bilinear')
    pyplot.figure()
    pyplot.axis('off')
    wc.to_file(r'../static/images/wc.png')

    

def countFinalWordsList(text,new_text):
    new_words=new_text.split(' ')
    countvaluelist=[]
    for i in new_words:
        #print i
        count=text.count(i)
        countvaluelist.append(count)
        
    funnel = Funnel("论坛评论词云统计图", width=900, height=700, title_pos='center')
    funnel.add(
        "论坛评论词云统计",
        new_words,
        countvaluelist,
        is_label_show=True,
        label_pos="inside",
        label_text_color="#fff",
        funnel_sort="escending"
    )
    funnel.render(r'../templates/ciyuncountwords.html')
    

if __name__=='__main__':
    countCiYun()
    
    
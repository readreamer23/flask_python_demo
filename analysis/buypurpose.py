#coding:utf-8
from pyecharts import Bar
import pymongo
import sys

#柱形图

reload(sys)
sys.setdefaultencoding('utf-8')

client=pymongo.MongoClient(host='127.0.0.1', port=27017)
comments = client.qichezhijia.qichezhijia1
print('数据记录条数count:', comments.estimated_document_count())
cursor = comments.find()
text = ''.join(map(lambda doc: doc.get('comment'), cursor))

attr = ["上下班","接小孩","购物","自驾游","拉货","约会","商务接送"]
v1 = [0,0,0,0,0,0,0]
for index,i in enumerate(attr):
    attri=attr[index]
    print attri
    count=text.count(attri)
    v1[index]=count
    
print v1
bar = Bar("荣威RX5购车目的统计示例图")
bar.add("荣威RX5购车目的统计", attr, v1, is_stack=True)
bar.render(r'../templates/buypurpose.html')


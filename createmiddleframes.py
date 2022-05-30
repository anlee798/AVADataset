# import pickle
# avaMin_dense_proposals_path = './dense_proposals_train.pkl'
# f = open(avaMin_dense_proposals_path,'rb')
# info = pickle.load(f, encoding='iso-8859-1') 
# print(info)
import os
import shutil
labelimgpath = './data/ava/labelframes' #表示需要命名处理的文件夹
middleimgpath = './data/ava/middleframes'
if not os.path.exists(middleimgpath):
    os.mkdir(middleimgpath)
dirname = ''
filelist = os.listdir(labelimgpath) #获取文件路径
for item in filelist:
    #src = os.path.join(os.path.abspath(labelimgpath), item)
    src = os.path.join(labelimgpath, item)
    temp_dirname = item.split('_')[0] ## A or B
    if temp_dirname==dirname:
        shutil.copy(src, os.path.join(middleimgpath, dirname))
    else:
        dirname = temp_dirname
        newpathframes = os.path.join(middleimgpath, dirname)
        if not os.path.exists(newpathframes):
            os.mkdir(newpathframes)

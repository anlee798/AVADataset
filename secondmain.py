'''
    target:一键生成AVA数据集(两部分)
        part1:Via标注前的工作 --> 生成检测的图片,并框好图片中人的位置
            VIA标注  --> 标记好动作类别 导出放在下面json位置 并以.._fininsh.json命名
        part2:Via标注后的工作  --> 使用deepsort检测每个人的id 合并到一个csv文件夹下 并生成Annotations文件夹及其所需的所有数据文件
    author:AnLee

AVADATASET
│── Annotations 最后生成的所有文件 可以直接拿到mmaction2下进行训练
├── choose_frames 每隔1秒提取的一张图片,给YOLODeepSort检测使用
    ├──A
    ├──B
    ├──C
├── choose_frames_all 每隔1秒提取的一张图片 合并在一个文件夹
├── choose_frames_middle 不包含前两张和后两张 间隔一秒抽取的图片  json数据生成的地方
    ├──A
    ├──B
    ├──C
├── frames 每秒30帧抽取的数据
    ├──A.mp4
    ├──B.mp4
    ├──C.mp4
├── video_crop 剪切后的视频
├── videos 原视频
    ├──A.mp4
    ├──B.mp4
├── yolovDeepsort  
'''
## Run python secondmain.py

import os
import pandas as pd
startSecond = 2
endSecond = 8


def deleteNullRow(start,end):
    #删除csv文件的空行
    data = pd.read_csv(start)
    res = data.dropna(how="all")
    res.to_csv(end, index=False)

#提取via标注好的JSON文件信息
os.system('python ./json_extract.py')
deleteNullRow("./train_without_personID_temp.csv","./train_without_personID.csv")

#使用deep sort来关联人的ID
os.system('python ./yolovDeepsort/yolov5_to_deepsort.py --source ./frames')
deleteNullRow("./train_personID_temp.csv","./train_personID.csv")

# 融合actions与personID
# train_personID.csv  <==>  train_without_personID.csv
os.system('python train_temp.py')
deleteNullRow("./train_temp_temp.csv","./train_temp.csv")

#第一次出现 人的ID很多值为负数
os.system('python train.py')
deleteNullRow("./train_temp.csv","./train.csv")

#Annotation文件夹填充
os.system('touch ./Annotations/train_excluded_timestamps.csv')
os.system('touch ./Annotations/included_timestamps.txt')
path = './Annotations/included_timestamps.txt'
file = open(path,'w+')
for i in range(startSecond,endSecond+1):
    file.write(str(i))
    file.write('\n')
file.close()
os.system('touch ./Annotations/action_list.pbtxt')
path = './Annotations/action_list.pbtxt'
file = open(path,'w+')
file.write('asd')
file.close()

#拷贝train.csv文件到Annotations
os.system('cp ./train.csv ./Annotations')
os.system('cp ./Annotations/train.csv ./Annotations/val.csv')

#拷贝dense_proposals_train.pkl到Annotations
os.system('cp ./yolovDeepsort/mywork/dense_proposals_train.pkl ./Annotations')
os.system('cp ./Annotations/dense_proposals_train.pkl ./Annotations/dense_proposals_val.pkl')

os.system('cp ./Annotations/train_excluded_timestamps.csv ./Annotations/val_excluded_timestamps.csv')

os.system('cp -r ./frames/* ./Annotations/rawframes')

os.system('python ./change_raw_frames.py')

#有部分的标注文件在字段类型上有些问题
os.system('python ./yolovDeepsort/mywork/change_dense_proposals_train.py')
os.system('python ./yolovDeepsort/mywork/change_dense_proposals_val.py')
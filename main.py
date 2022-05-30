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
'''
参数：
cut_videos.sh  修改剪切的时间  从哪一秒开始  剪切多少秒
'''
##运行 python main.py
import os
#裁剪原视频
os.system('bash cut_videos.sh')

#视频抽帧
os.system('bash cut_frames.sh')

#先抽取后的视频帧（间隔30帧） 再合并所有抽取的视频帧  便于YOLO检测
#其中10代表视频长度，0代表从第0秒开始
os.system('python choose_frames_all.py 10 0')

# 抽取视频帧（间隔30帧） 但是不合并 便于via标注
os.system('python choose_frames.py 10 0')

#使用YOLO检测视频中的物体 对choose_frames_all进行检测  ==>  ./yolovDeepsort/yolov5/runs/detect/exp
os.system('python ./yolovDeepsort/yolov5/detect.py --source ./choose_frames_all/ --save-txt --save-conf')

#生成dense_proposals_train.pkl
os.system('python ./yolovDeepsort/mywork/dense_proposals_train.py ./yolovDeepsort/yolov5/runs/detect/exp/labels ./yolovDeepsort/mywork/dense_proposals_train.pkl show')

# 生成choose_frames_all_middle文件夹 创建一个choose_frames_middle文件夹，存放不含前2张图片与后2张图片的文件夹
os.system('python choose_frames_middle.py')

#生成via标注文件 .json
os.system('python ./pkl2json.py ./yolovDeepsort/mywork/dense_proposals_train.pkl ./choose_frames_middle/')

#移除json标注默认值
os.system('python ./chang_via_json.py')
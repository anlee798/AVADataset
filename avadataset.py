import os
#运行本脚本  python avadataset.py

#切割视频，生成图片
#os.system('python ./data/ava/video2img.py')

#使用YOLO检测视频中的物体【Done】
# (mmact) E:\ActionDetection\AVADataSet\yolovDeepsort>
#python ./yolov5/detect.py --source ../data/ava/labelframes/ --save-txt --save-conf
#os.system('python ./yolovDeepsort/yolov5/detect.py --source ./data/ava/labelframes/ --save-txt --save-conf')

#生成dense_proposals_train.pkl【Done】
#os.system('python ./yolovDeepsort/mywork/dense_proposals_train.py ./yolovDeepsort/yolov5/runs/detect/exp/labels ./yolovDeepsort/mywork/dense_proposals_train.pkl show')

#生成middleframes文件夹
#os.system('python createmiddleframes.py')

#生成via标注文件 .json
#cd /home/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset/yolovDeepsort/mywork/
#python dense_proposals_train_to_via.py ./dense_proposals_train.pkl ../../Dataset/choose_frames_middle/
#os.system('python ./yolovDeepsort/mywork/dense_proposals_train_to_via.py ./yolovDeepsort/mywork/dense_proposals_train.pkl ./data/ava/middleframes/')

#去掉via默认值
#os.system('python ./data/ava/chang_via_json.py')

os.system('python ./data/ava/tt.py')

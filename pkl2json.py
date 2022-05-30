'''
Run python pkl2json.py
'''
import pickle
from via3_tool import Via3Json
import os
import cv2
from collections import defaultdict

f = open('./dense_proposals_train.pkl','rb')
info = pickle.load(f, encoding='iso-8859-1') 
dirname = ''
json_path = './choose_frames_middle/'
attributes_dict = {'1':dict(aname='head', type=2, options={'0':'talk',
                   '1':'bow'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),

                   '2': dict(aname='body', type=2, options={'0':'stand',
                   '1':'sit', '2':'walk'}, default_option_id="", anchor_id='FILE1_Z0_XY1'),
                   
                  '3':dict(aname='limbs', type=2, options={'0':'smokeing',
                   '1':'call phone'},default_option_id="", anchor_id = 'FILE1_Z0_XY1'),
                  }
dirflod = {}
for root, dirs, files in os.walk(json_path, topdown=False):
    ls = []
    for file in files:
        if '.jpg' in file:
            index = file.split('_')[1].split('.')[0]
            ls.append(int(index))
    if ls == []:
        break
    dirflod[file.split('_')[0]] = ls
print(dirflod)
curflordindex = 0
for i in info:
    #print("i:",i,"||","info[i]",info[i])
    temp_dirname = i.split(',')[0]
    temp_index = int(i.split(',')[1])
    if temp_dirname in dirflod.keys():
        if not temp_index in dirflod.get(temp_dirname):
            continue 
    curflordindex += 1
    if dirname == temp_dirname:
        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(curflordindex),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            #print(metadata_dict)
            metadatas_dict['image{}_{}'.format(curflordindex,vid)] = metadata_dict
        if curflordindex == len(dirflod.get(temp_dirname)):
            via3.dumpMetedatas(metadatas_dict)
            views_dict = {}
            for i, vid in enumerate(vid_list,1):
                views_dict[vid] = defaultdict(list)
                views_dict[vid]['fid_list'].append(str(i))
            via3.dumpViews(views_dict)
            via3.dempJsonSave()
            via3.dempJsonSave()

    else:
        curflordindex = 1
        dirname = temp_dirname
        #print("dirname",dirname)
        temp_json_path = './choose_frames_middle/' + dirname + '/' + dirname + '_proposal.json'
        via3 = Via3Json(temp_json_path, mode='dump')
        imgcount = 0
        files_dict,  metadatas_dict = {},{}
        for root, dirs, files in os.walk(json_path + dirname, topdown=False):
            for file in files:
                if '.jpg' in file:
                    imgcount+=1
                    files_dict[str(imgcount)] = dict(fname=file, type=2)

                    temp_img_path = json_path + dirname +'/' + file #图片路径
                    img = cv2.imread(temp_img_path)  #读取图片信息
                    sp = img.shape #[高|宽|像素值由三种原色构成]
                    img_H = sp[0]
                    img_W = sp[1]
        vid_list = list(map(str,range(1, imgcount+1)))
        via3.dumpPrejects(vid_list)
        via3.dumpConfigs()
        via3.dumpAttributes(attributes_dict)
        via3.dumpFiles(files_dict)


        for vid,result in enumerate(info[i],1):
            xyxy = result
            xyxy[0] = img_W*xyxy[0]
            xyxy[2] = img_W*xyxy[2]
            xyxy[1] = img_H*xyxy[1]
            xyxy[3] = img_H*xyxy[3]
            temp_w = xyxy[2] - xyxy[0]
            temp_h = xyxy[3] - xyxy[1]
            
            metadata_dict = dict(vid=str(curflordindex),
                                 xy=[2, float(xyxy[0]), float(xyxy[1]), float(temp_w), float(temp_h)],
                                 av={'1': '0'})
            #print(metadata_dict)
            metadatas_dict['image{}_{}'.format(curflordindex,vid)] = metadata_dict
        via3.dumpMetedatas(metadatas_dict)
        #print("metadatas_dict",metadatas_dict)
        #{'image1_1': {'vid': '1', 'xy': [2, 422.0, 128.00016, 344.9996800000001, 555.99984], 'av': {'1': '0'}},
         #'image1_2': {'vid': '1', 'xy': [2, 984.9996799999999, 115.00020000000004, 292.9996800000001, 586.00008], 'av': {'1': '0'}}}

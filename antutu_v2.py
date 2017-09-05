import cv2
import os
import os.path
import numpy as np
from matplotlib import pyplot as plt

#获取两个图片匹配坐标
def get_copoint(path1,path2):
    tuple = ()
    img = cv2.imread(path1,0)
    template = cv2.imread(path2,0)
    #template = cv2.resize(template,None,fx=1, fy=1, interpolation = cv2.INTER_CUBIC) 图片缩放
    w, h = template.shape[::-1]
    tuple = (w,h)
    methods = 'cv2.TM_SQDIFF_NORMED'
    method = eval(methods)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 0, 2)
    print(top_left,bottom_right)

    return top_left,bottom_right,tuple

#计算所有坐标及其中心点
def get_colist(tapdir,rootdir,list1,list2):
    co_left = []
    co_right = []
    tup = ()
    tup_wh = ()
    co = []
    box = []
    flag = 1
    for i in range(0,3):
        path = os.path.join(tapdir, list1[i])
        co_left, co_right, tup_wh= get_copoint(os.path.join('screencap_box', 'screen.png'), path)
        tup = ((co_left[0] + co_right[0]) / 2, (co_left[1] + co_right[1]) / 2)
        co.append(tup)
    i = 0
    for i in range(0, len(list2)):
        path = os.path.join(rootdir, list2[i])
        if flag == 1:
            co_left, co_right, tup_wh = get_copoint(os.path.join('screencap_box', 'ppp.png'), path)
            tup = ((co_left[0] + co_right[0]) / 2, (co_left[1] + co_right[1]) / 2)
            co.append(tup)
            box.append(co_left)
            box.append(tup_wh)
            flag = flag + 1
            i-=1
            continue
        if flag == 2:
            co_left, co_right, tup_wh = get_copoint(os.path.join('screencap_box', 'png1.png'), path)
            tup = ((co_left[0] + co_right[0]) / 2, (co_left[1] + co_right[1]) / 2)
            co.append(tup)
            box.append(co_right)
            box.append(tup_wh)
            if i == 3:
                flag +=1
                i-=1
                continue
        if flag == 3:
            co_left, co_right, tup_wh= get_copoint(os.path.join('screencap_box', 'png2.png'), path)
            tup = ((co_left[0] + co_right[0]) / 2, (co_left[1] + co_right[1]) / 2)
            co.append(tup)
            box.append(co_right)
            box.append(tup_wh)
            if i == 9:
                flag += 1
                i-=1
                continue
        if flag == 4:
            co_left, co_right, tup_wh  = get_copoint(os.path.join('screencap_box', 'png3.png'), path)
            tup = ((co_left[0] + co_right[0]) / 2, (co_left[1] + co_right[1]) / 2)
            co.append(tup)
            box.append(co_right)
            box.append(tup_wh)
    return co,box

#写入flow.txt
def get_txt(co):
    print (co)
    with open('flow_1920.txt', 'w') as f:
        f.write('am start com.antutu.ABenchMark/.ABenchMarkStart' + '\n')
        f.write('sleep 5' + '\n')
        f.write('input tap %d %d' % (co[3][0], co[3][1]) + '\n')
        f.write('sleep 360' + '\n')
        f.write('input tap %d %d' % (co[0][0], co[0][1]) + '\n')
        f.write('screencap png1.png' + '\n')
        f.write('input tap %d %d' % (co[0][0], co[0][1]) + '\n')
        f.write('input tap %d %d' % (co[1][0], co[1][1]) + '\n')
        f.write('screencap png2.png' + '\n')
        f.write('input tap %d %d' % (co[1][0], co[1][1]) + '\n')
        f.write('input tap %d %d' % (co[2][0], co[2][1]) + '\n')
        f.write('input swipe 600 600 200 200' + '\n')
        f.write('screencap png3.png' + '\n')
        f.write('input tap %d %d' % (co[2][0], co[2][1]) + '\n')

#计算截图中数字区域
def get_box(box):
    box_list = []
    j = 2
    tuple = ()
    tuple = (box[0][0],(box[0][1]-100),(box[0][0]+220),box[0][1])
    box_list.append(tuple)
    for i in range(1,15):
        tuple = (box[j][0],(box[j][1]-box[j+1][1]),(box[j][0]+200),box[j][1])
        box_list.append(tuple)
        j+=2
    print (box_list)
    #test_re(box_list)
    return box_list

#用于测试box_list的准确性
def test_re(box_list):
    for i in range(10,15):
        img = cv2.imread(os.path.join('screencap_box', 'png3.png'), 0)
        top_left = (box_list[i][0],box_list[i][1])
        bottom_right = (box_list[i][2],box_list[i][3])
        cv2.rectangle(img, top_left, bottom_right, 0, 2)
        cv2.namedWindow("Image")
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
#主函数
if __name__ == '__main__':
    tapdir = os.path.join('tap_box')
    rootdir = os.path.join('template_box')
    list1 = os.listdir(tapdir)
    list2 = os.listdir(rootdir)
    co = []
    box = []
    co,box = get_colist(tapdir, rootdir, list1, list2)
    get_txt(co)
    get_box(box)












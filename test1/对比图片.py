#!/usr/bin/python
# coding : utf-8

import aircv as ac
import cv2 as cv

def matchImg(imgsrc,imgobj,confidence=0.5):#imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)

    match_result = ac.find_template(imsrc,imobj,confidence)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

    return match_result

aaa = matchImg(imgsrc='/Users/iyunshu/Desktop/测试2.png', imgobj='/Users/iyunshu/Desktop/测试.png')

print(aaa)
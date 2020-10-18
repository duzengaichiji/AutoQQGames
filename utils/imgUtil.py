import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image


#获取一张完整的屏幕截图
def ScreenGrab():
    #print("获取屏幕截图..")
    scim = ImageGrab.grab() #屏幕截图
    scim.save('../images/zhaoCha/screen.png')
    return cv2.imread('../images/zhaoCha/screen.png') #返回截图


#获取应用窗口的完整截图
def WindowGrab():
    pass




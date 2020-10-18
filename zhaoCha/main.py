from tkinter import *
from PIL import Image, ImageTk
from zhaoCha import config
from utils.imgUtil import *
from utils.windowUtil import *
import pyautogui as pag

def getAllSquare(screenImg, windowPos, firstOffset, secondOffset, ImgSize):
    """
    Args:
        ImgSize: 找茬中单个图片的大小
        screenImg: 屏幕截图
        windowPos: 窗口起点位置
        firstOffset: 第一张图片的偏移量
        secondOffset: 第二张图片的偏移量
    Returns:
        对目标区域切片的所有方块
    """
    first_x = windowPos[0]+firstOffset[0]
    first_y = windowPos[1]+firstOffset[1]
    second_x = windowPos[0]+secondOffset[0]
    #second_y = windowPos[1]+secondOffset[1]
    # 找茬中左右两张图
    screenImgLeft = screenImg[first_y:first_y+ImgSize[1], first_x:first_x+ImgSize[0]]
    screenImgRight = screenImg[first_y:first_y+ImgSize[1], second_x:second_x+ImgSize[0]]
    return screenImgLeft, screenImgRight

def getDiff(leftImg, rightImg):
    """

    Args:
        leftImg: 原图
        rightImg: 另外一幅图
        config: 算法配置

    Returns:
        像素不同的数组
    """
    width = leftImg.shape[0]
    height = leftImg.shape[1]

    flags = abs(leftImg-rightImg)
    flags[:, :, 0] = (flags[:, :, 0] > config.rThreshold).astype(np.int32)
    flags[:, :, 1] = (flags[:, :, 1] > config.gThreshold).astype(np.int32)
    flags[:, :, 2] = (flags[:, :, 2] > config.bThreshold).astype(np.int32)
    result = flags[:, :, 0]*flags[:, :, 1]*flags[:, :, 2]
    result_img = leftImg.copy()
    result_img[result==1, :] = [0, 215, 0]
    return result_img


def labelClick(event):
    """
    绑定鼠标点击事件到某个组件上
    Args:
        event:
    Returns:

    """
    refindWindow()
    global gameWindow, windowPos
    x0 = event.x
    y0 = event.y
    win32gui.SetForegroundWindow(gameWindow)  # 将窗口置顶

    x, y = pag.position()
    x1 = x0+windowPos[0]+config.FIRST_IMAGE_X_OFFSET
    y1 = y0+windowPos[1]+config.FIRST_IMAGE_Y_OFFSET
    mouseClick(x1, y1)
    moveMouseTo(x, y)


def refindWindow():
    global gameWindow, windowPos
    gameWindow, windowPos = getGameWindowPosition(WINDOW_TITLE=config.WINDOW_TITLE)
    #print(windowPos)

def help():
    """
    点击更换到当前的图片
    Returns:

    """
    refindWindow()
    global gameWindow, windowPos
    win32gui.SetForegroundWindow(gameWindow)  # 将窗口置顶
    scim = ScreenGrab()
    leftscim, rightscim = getAllSquare(scim, [windowPos[0], windowPos[1]], [config.FIRST_IMAGE_X_OFFSET, config.FIRST_IMAGE_Y_OFFSET],
                           [config.SECOND_IMAGE_X_OFFSET, config.SECOND_IMAGE_X_OFFSET], [config.IMG_WIDTH, config.IMG_HEIGHT])
    diff = getDiff(leftscim, rightscim)
    Image.fromarray(diff).save('../images/zhaoCha/diff.png')
    diff = ImageTk.PhotoImage(Image.open("../images/zhaoCha/diff.png"))
    imglabel.configure(image=diff)
    imglabel.image = diff
    imglabel.grid(row=0, columnspan=2)

def exit():
    print("退出，释放资源")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    root.destroy()


if __name__ == '__main__':
    #定位窗体位置
    gameWindow, windowPos = getGameWindowPosition(WINDOW_TITLE=config.WINDOW_TITLE)

    root = Tk()
    root.iconbitmap('../images/myico.ico')
    root.title('大家一起来找茬')
    root.protocol('WM_DELETE_WINDOW', exit) # 绑定窗口销毁事件

    img = Image.open('../images/zhaoCha/default.png')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 转为支持格式
    imglabel = Label(root, image=photo)
    imglabel.bind('<Button-1>', labelClick) # 为组件绑定左键单击事件
    imglabel.grid(row=0, columnspan=2)

    btnHelp = Button(root, text="获取不同区域", width=20, height=2, command=help)
    btnHelp.grid(row=1, column=0)
    btnRefind = Button(root, text="重定位窗口位置", width=20, height=2, command=refindWindow)
    btnRefind.grid(row=1, column=1)
    mainloop()

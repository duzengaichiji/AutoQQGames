import cv2
import numpy as np
import win32api
import win32gui
import win32con
import time


def getGameWindowPosition(className=None, WINDOW_TITLE=None):
    """

    Args:
        className:
        WINDOW_TITLE: 窗口的句柄

    Returns:
        窗口对象，窗口左上角的x，y坐标
    """
    if WINDOW_TITLE is None:
        print("未指定窗口名称")
    window = win32gui.FindWindow(className, WINDOW_TITLE)
    retries = 5
    while not window and retries<=0:
        print("定位窗体失败")
        retries -= 1
        time.sleep(1)
        window = win32gui.FindWindow(className, WINDOW_TITLE)
    pos = win32gui.GetWindowRect(window) #[x起点，y起点，窗口宽度，窗口长度]
    return window, (pos[0], pos[1])


def setGameWindowForeground(window):
    """
    将指定窗口前置
    Args:
        window:

    Returns:

    """
    win32gui.SetForegroundWindow(window)    #将窗口置顶


def moveMouseTo(xPos, yPos):
    """
    将鼠标移动到指定位置
    Args:
        xPos:
        yPos:

    Returns:

    """
    win32api.SetCursorPos((xPos, yPos))


def mouseClick(xPos, yPos, interval=0.1):
    """
    模拟一次鼠标点击
    Args:
        xPos: 点击位置的x坐标
        yPos: 点击位置的y坐标
        interval: 点击间隔

    Returns:

    """
    moveMouseTo(xPos, yPos)
    time.sleep(interval)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xPos, yPos, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xPos, yPos, 0, 0)

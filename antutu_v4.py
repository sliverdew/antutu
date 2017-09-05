import re
import os
import time
from openpyxl import Workbook
from pyadb import adb
from xml.dom import minidom
import shutil


# 从xml页面中提取分数
def get_score(path):
    score = []
    dom = minidom.parse(path)
    root = dom.documentElement
    nodes = root.getElementsByTagName('node')
    for node in nodes:
        score_node = node.getAttribute('resource-id')
        if score_node == 'com.antutu.ABenchMark:id/tv_score':
            text = node.getAttribute('text')
            # bound = node.getAttribute('bounds')
            score.append(text)
    return score


# 从xml中提取点击坐标

def get_xml(path, pattern):
    px = 0
    py = 0
    if path == '1.xml':
        dom = minidom.parse(path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        for node in nodes:
            score_node = node.getAttribute('resource-id')
            if score_node == 'com.antutu.ABenchMark:id/tv_score':
                bound = node.getAttribute('bounds')
                x, y = eval(re.sub("\]\[", "],[", bound))
                px = (x[0] + y[0]) / 2
                py = (x[1] + y[1]) / 2
                return px, py
    dom = minidom.parse(path)
    root = dom.documentElement
    nodes = root.getElementsByTagName('node')
    for node in nodes:
        text = node.getAttribute('text')
        if text == pattern:
            bound = node.getAttribute('bounds')
            print(bound)
            x, y = eval(re.sub("\]\[", "],[", bound))
            px = (x[0] + y[0]) / 2
            py = (x[1] + y[1]) / 2
            print(px, py)
    return px, py


# 返回提取到的坐标

def operation(pattern):
    score = []
    adb.shell('uiautomator dump /sdcard/2.xml')
    time.sleep(2)
    adb.pull('/sdcard/2.xml', os.getcwd())
    px, py = get_xml('2.xml', pattern)
    adb.shell('input tap ' + str(px) + ' ' + str(py))
    adb.shell('uiautomator dump /sdcard/3.xml')
    time.sleep(2)
    adb.pull('/sdcard/3.xml', os.getcwd())
    score = get_score('3.xml')
    px, py = get_xml('3.xml', pattern)
    adb.shell('input tap ' + str(px) + ' ' + str(py))

    return score


def score_operate():
    score_match = []
    adb.shell('am start com.antutu.ABenchMark/.ABenchMarkStart')
    time.sleep(10)
    adb.shell('uiautomator dump /sdcard/6.xml')
    time.sleep(2)
    adb.pull('/sdcard/6.xml', os.getcwd())
    #shutil.copy('1.xml','6.xml')
    oper_px,oper_py = get_xml('6.xml','重新测试')
    adb.shell('input tap ' + str(oper_px) + ' ' + str(oper_py))
    time.sleep(400)
    total_px, total_py = get_xml('1.xml', 0)
    total_score = get_score('1.xml')
    adb.shell('input tap ' + str(total_px) + ' ' + str(total_py))
    time.sleep(1)
    adb.shell('input tap ' + str(total_px) + ' ' + str(total_py))
    time.sleep(1)
    score_match = score_match + total_score

    ddd_score = operation('3D性能')
    score_match = score_match + ddd_score
    time.sleep(2)

    ux_score = operation('UX性能')
    score_match = score_match + ux_score
    time.sleep(2)

    cpu_score = operation('CPU性能')
    score_match = score_match + cpu_score
    time.sleep(2)

    adb.shell('uiautomator dump /sdcard/8.xml')
    time.sleep(2)
    adb.pull('/sdcard/8.xml', os.getcwd())
    ram_score = get_score('8.xml')
    score_match = score_match + ram_score

    return score_match

if __name__ == '__main__':
    # 写excel第一行
    wb = Workbook()
    ws = wb.active
    ws.append(['Total',
               '3D',
               '3D[Graden]',
               '3D[Marooned]',
               'UX',
               'UX Data Secure',
               'UX Data Process',
               'UX Strategy games',
               'UX Image process',
               'UX I/O performance',
               'CPU',
               'CPU Mathematics',
               'CPU Common Use',
               'CPU Multi-Core',
               'RAM'])  # 添加所需数据名称

    score_match = score_operate()
    print(score_match)
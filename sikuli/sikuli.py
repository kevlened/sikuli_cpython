import os
import sys

if sys.platform == 'win32':
    separator = ';'
else:
    separator = ':'
    
javapath = separator + os.path.dirname(os.path.realpath(__file__)) + "/sikuli-api-1.0.2-standalone.jar"
if not 'CLASSPATH' in os.environ:
    os.environ['CLASSPATH'] = javapath
else:
    os.environ['CLASSPATH'] += javapath

from jnius import autoclass

File = autoclass('java.io.File')
URL = autoclass('java.net.URL')

DesktopMouse = autoclass('org.sikuli.api.robot.desktop.DesktopMouse')
DesktopKeyboard = autoclass('org.sikuli.api.robot.desktop.DesktopKeyboard')

API = autoclass('org.sikuli.api.API')
DesktopScreenRegion = autoclass('org.sikuli.api.DesktopScreenRegion')
ImageTarget = autoclass('org.sikuli.api.ImageTarget')


def find(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    x = d.find(t)
    return x


def findAll(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    x = d.findAll(t)
    return x


def wait(target, duration=5000):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    x = d.wait(t, duration)
    return x


# TODO: waitVanish


def exists(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    try:
        x = d.find(t)
    except Exception:
        x = None

    return x
    

def click(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    item = d.find(t)
    m = DesktopMouse()
    m.click(item.getCenter())


def doubleClick(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    item = d.find(t)
    m = DesktopMouse()
    m.doubleClick(item.getCenter())


def rightClick(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    item = d.find(t)
    m = DesktopMouse()
    m.rightClick(item.getCenter())


def hover(target):
    t = ImageTarget(File(target))
    d = DesktopScreenRegion()
    item = d.find(t)
    m = DesktopMouse()
    m.hover(item.getCenter())


# TODO: dragDrop


def type(text):
    k = DesktopKeyboard()
    k.type(text)


def paste(text):
    k = DesktopKeyboard()
    k.paste(text)


def browse(url):
    API.browse(URL(url))
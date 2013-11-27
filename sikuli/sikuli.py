import os
import sys

if sys.platform == 'win32':
    separator = ';'
else:
    separator = ':'
    
jarpath = separator + os.path.dirname(os.path.realpath(__file__)) + "/sikuli-api-1.0.2-standalone.jar"
if not 'CLASSPATH' in os.environ:
    os.environ['CLASSPATH'] = jarpath
else:
    os.environ['CLASSPATH'] += jarpath

from jnius import autoclass

File = autoclass('java.io.File')
URL = autoclass('java.net.URL')

DesktopMouse = autoclass('org.sikuli.api.robot.desktop.DesktopMouse')
DesktopKeyboard = autoclass('org.sikuli.api.robot.desktop.DesktopKeyboard')

API = autoclass('org.sikuli.api.API')
DesktopScreenRegion = autoclass('org.sikuli.api.DesktopScreenRegion')
ImageTarget = autoclass('org.sikuli.api.ImageTarget')


def find(target_string, *args, **kwargs):
    target = _get_target_from_string(target_string, *args, **kwargs)
    screen = DesktopScreenRegion()
    return screen.find(target)


def findAll(target_string, *args, **kwargs):
    target = _get_target_from_string(target_string, *args, **kwargs)
    screen = DesktopScreenRegion()
    return screen.findAll(target)


def wait(target_string, *args, **kwargs):
    if not duration and duration != 0:
        duration = 5000
    target = _get_target_from_string(target_string, *args, **kwargs)
    screen = DesktopScreenRegion()
    return screen.wait(target, duration)


# TODO: waitVanish


def exists(target_string, *args, **kwargs):
    target = _get_target_from_string(target_string, *args, **kwargs)
    screen = DesktopScreenRegion()
    try:
        t = screen.find(target)
    except Exception:
        t = None

    return t
    

def click(target_string, *args, **kwargs):
    t = _get_screen_loc(target_string, *args, **kwargs)
    m = DesktopMouse()
    m.click(t)


def doubleClick(target_string, *args, **kwargs):
    t = _get_screen_loc(target_string, *args, **kwargs)
    m = DesktopMouse()
    m.doubleClick(t)


def rightClick(target_string, *args, **kwargs):
    t = _get_screen_loc(target_string, *args, **kwargs)
    m = DesktopMouse()
    m.rightClick(t)


def hover(target_string, *args, **kwargs):
    t = _get_screen_loc(target_string, *args, **kwargs)
    m = DesktopMouse()
    m.hover(t)


def dragDrop(target_string_1, target_string_2):
    loc1 = _get_screen_loc(target_string_1)
    loc2 = _get_screen_loc(target_string_2)
    m = DesktopMouse()
    m.drag(loc1)
    m.drop(loc2)


def type(text):
    k = DesktopKeyboard()
    k.type(text)


def paste(text):
    k = DesktopKeyboard()
    k.paste(text)


def browse(url):
    API.browse(URL(url))


def _get_screen_loc(target_string, *args, **kwargs):
    t = find(target_string, *args, **kwargs)
    return t.getCenter()  


def _get_target_from_string(target_string, *args, **kwargs):
    target_file_loc = _find_local_file(target_string)
    if not target_file_loc:
        try:        
            target_file_loc = URL(target_string)
        except:
            target_file_loc = None
                        
    return ImageTarget(target_file_loc)


def _find_local_file(target_string):
    
    # Check the relative path
    poss_relative_path = os.path.join(os.getcwd(), target_string)
    if os.path.exists(poss_relative_path):
        return File(poss_relative_path)
        
    # Check the absolute path
    elif os.path.exists(target_string):
        return File(target_string)    
    
    else:
        return None
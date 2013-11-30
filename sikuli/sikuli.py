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
    target = Pattern(target_string).getTarget()
    screen = DesktopScreenRegion()
    return screen.find(target)


def findAll(target_string, *args, **kwargs):
    target = Pattern(target_string).getTarget()
    screen = DesktopScreenRegion()
    return screen.findAll(target)


def wait(target_string, *args, **kwargs):
    if not duration and duration != 0:
        duration = 5000
    target = Pattern(target_string).getTarget()
    screen = DesktopScreenRegion()
    return screen.wait(target, duration)


# TODO: waitVanish


def exists(target_string, *args, **kwargs):
    target = Pattern(target_string).getTarget()
    screen = DesktopScreenRegion()
    try:
        return screen.find(target)
    except Exception:
        return None


def click(target_string, *args, **kwargs):
    loc = Pattern(target_string).getLocation()
    m = DesktopMouse()
    m.click(loc)


def doubleClick(target_string, *args, **kwargs):
    loc = Pattern(target_string).getLocation()
    m = DesktopMouse()
    m.doubleClick(loc)


def rightClick(target_string, *args, **kwargs):
    loc = Pattern(target_string).getLocation()
    m = DesktopMouse()
    m.rightClick(loc)


def hover(target_string, *args, **kwargs):
    loc = Pattern(target_string).getLocation()
    m = DesktopMouse()
    m.hover(loc)


def dragDrop(target_string_1, target_string_2):
    loc1 = Pattern(target_string_1).getLocation()
    loc2 = Pattern(target_string_2).getLocation()
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


class Pattern:
    def __init__(self, target_string):
        if isinstance(target_string, Pattern):
            p = target_string
            self.target_string = p.target_string
            self.similarity = p.similarity
            self.dx, self.dy = p.dx, p.dy
        else:
            self.target_string = target_string
            self.similarity = .7
            self.dx, self.dy = 0, 0


    def exact(self):
        self.similarity = 0.99
        return self


    def targetOffset(self, x, y):
        self.dx, self.dy = x, y
        return self


    def similar(self, similarity):
        self.similarity = similarity
        return self


    def getTarget(self):
        return self._get_target_from_string(self.target_string)


    def getLocation(self):
        t = self.getTarget()
        region = find(self)
        loc = region.getCenter()
        loc.setX(loc.getX() + self.dx)
        loc.setY(loc.getY() + self.dy)
        return loc


    def _get_target_from_string(self, target_string):
        target_file_loc = self._find_local_file(target_string)
        if not target_file_loc:
            try:
                target_file_loc = URL(target_string)
            except:
                target_file_loc = None
        target = ImageTarget(target_file_loc)
        target.setMinScore(self.similarity)
        return target


    def _find_local_file(self, target_string):

        # Check the relative path
        poss_relative_path = os.path.join(os.getcwd(), target_string)
        if os.path.exists(poss_relative_path):
            return File(poss_relative_path)

        # Check the absolute path
        elif os.path.exists(target_string):
            return File(target_string)

        else:
            return None
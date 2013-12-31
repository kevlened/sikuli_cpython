import os
import sys

if sys.platform == 'win32':
    separator = ';'
else:
    separator = ':'

jarpath = separator + os.path.dirname(os.path.realpath(__file__)) + "/sikuli-api-1.0.3-standalone.jar"
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

class Sikuli:
    def __init__(self, **kwargs):
        if 'similarity' in kwargs:
            self.similarity = kwargs['similarity']
        else:
            self.similarity = 0.7

        if 'wait_timeout' in kwargs:
            self.wait_timeout = kwargs['wait_timeout']
        else:
            self.wait_timeout = 5000

    def find(self, target_string, *args, **kwargs):
        target = Pattern(target_string).similar(self.similarity).getTarget()
        screen = DesktopScreenRegion()
        return screen.find(target)

    def findAll(self, target_string, *args, **kwargs):
        target = Pattern(target_string).similar(self.similarity).getTarget()
        screen = DesktopScreenRegion()
        return screen.findAll(target)

    def wait(self, target_string, *args, **kwargs):
        duration = self.wait_timeout
        if 'timeout' in kwargs and kwargs['timeout'] > 0:
            duration = kwargs['timeout']
            target = Pattern(target_string).similar(self.similarity).getTarget()
            screen = DesktopScreenRegion()
            duration = 1
        return screen.wait(target, duration)


    # TODO: waitVanish


    def exists(self, target_string, *args, **kwargs):
        target = Pattern(target_string).similar(self.similarity).getTarget()
        screen = DesktopScreenRegion()
        try:
            return screen.find(target)
        except Exception:
            return None

    def click(self, target_string, *args, **kwargs):
        loc = Pattern(target_string).similar(self.similarity).getLocation()
        m = DesktopMouse()
        m.click(loc)

    def doubleClick(self, target_string, *args, **kwargs):
        loc = Pattern(target_string).similar(self.similarity).getLocation()
        m = DesktopMouse()
        m.doubleClick(loc)

    def rightClick(self, target_string, *args, **kwargs):
        loc = Pattern(target_string).similar(self.similarity).getLocation()
        m = DesktopMouse()
        m.rightClick(loc)

    def hover(self, target_string, *args, **kwargs):
        loc = Pattern(target_string).similar(self.similarity).getLocation()
        m = DesktopMouse()
        m.hover(loc)

    def dragDrop(self, target_string_1, target_string_2):
        pat1 = Pattern(target_string_1).similar(self.similarity)
        pat2 = Pattern(target_string_2).similar(self.similarity)
        loc1 = pat1.getLocation()
        loc2 = pat2.getLocation()
        m = DesktopMouse()
        m.drag(loc1)
        m.drop(loc2)

    def type(self, text):
        k = DesktopKeyboard()
        k.type(text)

    def paste(self, text):
        k = DesktopKeyboard()
        k.paste(text)

    def browse(self, url):
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
            self.similarity = 0.7
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

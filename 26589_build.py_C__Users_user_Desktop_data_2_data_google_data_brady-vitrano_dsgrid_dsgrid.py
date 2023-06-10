from adapter import DockerAdapter
import os


class GridBuilder:

    def __init__(self):
        self.adapter = DockerAdapter()

    def is_installed(self):
        container = self.adapter.find_image('dsgrid/selenium-hub')
        return container

    def build(self, container):
        if container == 'chrome':
            directory = os.path.join('/usr/local/dsgrid', 'files', 'chrome')
            if not os.path.exists(directory):
                print "File not found"
                return False
            self.adapter.client.build(directory, 'dsgrid/chrome-node')
            return True

        if container == 'phantomjs':
            directory = os.path.join('/usr/local/dsgrid', 'files', 'phantomjs')
            if not os.path.exists(directory):
                print "File not found"
                return False
            self.adapter.client.build(directory, 'dsgrid/phantomjs-node')
            return True

        if container == 'firefox':
            directory = os.path.join('/usr/local/dsgrid', 'files', 'firefox')
            if not os.path.exists(directory):
                return False
            self.adapter.client.build(directory, 'dsgrid/firefox-node')
            return True

        if container == 'selenium-hub':
            directory = os.path.join('/usr/local/dsgrid', 'files', 'selenium')
            if not os.path.exists(directory):
                return False
            self.adapter.client.build(directory, 'dsgrid/selenium-hub')
            return True

        return False






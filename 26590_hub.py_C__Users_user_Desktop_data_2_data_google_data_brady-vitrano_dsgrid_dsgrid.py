import sys
from adapter import DockerAdapter


class HubController:
    def __init__(self):
        self.hub = GridHub()

    @staticmethod
    def is_running():
        hub = GridHub()
        return hub.is_running()

    @staticmethod
    def start():
        """
        @rtype: bool
        @return: True on success
        """
        hub = GridHub()
        try:
            hub.start()
            # TODO: Verify Started
            return True
        except Exception:
            return False

    @staticmethod
    def is_valid_browser(browser):

        if browser in GridHub.VALID_BROWSERS:
            return True
        return False

    @staticmethod
    def add(browser):
        """
        @type browser: string
        @param browser: Browser Name
        @rtype: bool
        @return: True on success
        """
        hub = GridHub()
        return hub.add_node(browser)

    @staticmethod
    def get_status():
        hub = GridHub()

        ff_count = 0
        ph_count = 0
        ch_count = 0

        nodes = hub.get_nodes()
        for node in nodes:
            if "firefox" in node['Image']:
                ff_count += 1
            elif "phantomjs" in node['Image']:
                ph_count +=1
            elif "chrome" in node['Image']:
                ch_count += 1

        status = {
            "Ip": hub.get_ip(),
            "firefox_count": ff_count,
            "phantomjs_count": ph_count,
            "chrome_count": ch_count
        }

        return status

    @staticmethod
    def restart_nodes(browser=None):
        hub = GridHub()
        return hub.restart_nodes(browser)

    @staticmethod
    def stop_nodes():
        hub = GridHub()
        return hub.stop_nodes()

    @staticmethod
    def shutdown():
        hub = GridHub()
        hub.shutdown()


class GridHub:
    VALID_BROWSERS = ('firefox', 'phantomjs', 'chrome')

    def __init__(self):
        self.adapter = DockerAdapter()

    def get_container_info(self):
        container = self.adapter.find_container('dsgrid/selenium-hub:latest')
        if not container:
            # raise exception container not found
            return False
        container_info = self.adapter.inspect(container['Id'])
        container = dict(container.items() + container_info.items())
        return container

    def get_nodes(self):
        nodes = []
        containers = self.adapter.client.containers()

        for container in containers:
            if "node" in container['Image']:
                nodes.append(container)

        return nodes

    def is_running(self):
        container = self.get_container_info()
        if not container:
            # raise exception container not found
            return False
        return "Up" in container['Status']

    def start(self):
        response = self.adapter.client.create_container('dsgrid/selenium-hub', ports={"4444/tcp": {}})
        if response['Id']:
            self.adapter.client.start(response, None, {'4444/tcp': ('', '49044')})

    def get_ip(self):
        container = self.get_container_info()
        return container['NetworkSettings']['IPAddress']

    def add_node(self, browser):
        if not browser in self.VALID_BROWSERS:
            return False
        ip = self.get_ip()
        response = self.adapter.client.create_container('dsgrid/'+browser+'-node', [], environment={"GRID_IP": ip})
        if response['Id']:
            self.adapter.client.start(response)
            return True

    def restart_nodes(self, browser=None):
        containers = self.get_nodes()
        nodes_to_stop = []
        for container in containers:
            if browser is not None and browser not in container['Image']:
                continue
            nodes_to_stop.append(container)

        if len(nodes_to_stop) == 0:
            return False

        for container in nodes_to_stop:
            self.adapter.restart(container)

        return True

    def stop_nodes(self, by_browser=None):
        if by_browser is not None and not by_browser in self.VALID_BROWSERS:
            # raise exception
            return False

        browser = ''
        if by_browser in self.VALID_BROWSERS:
            browser = by_browser + '-'

        containers = self.adapter.client.containers()

        for container in containers:
            if browser + "node" in container['Image']:
                self.adapter.client.stop(container['Id'])
                self.adapter.client.remove_container(container['Id'])

        return True

    def shutdown(self):

        self.stop_nodes()
        container = self.adapter.find_container('dsgrid/selenium-hub:latest')
        if not container:
            # raise exception container not found
            return False
        self.adapter.client.stop(container)
        self.adapter.client.remove_container(container)


import unittest
import docker
from dsgrid.hub import GridHub
from dsgrid.adapter import DockerAdapter


class TestDockerInterface(unittest.TestCase):
    def test_can_search_container(self):
        adapter = DockerAdapter()
        image = adapter.find_image('brady/selenium-grid')
        if not image:
            print "Not Found"
        print "Found"

    def test_can_check_if_grid_running(self):
        adapter = DockerAdapter()
        container = adapter.find_container('brady/selenium-grid:latest')
        if not container:
            print "Not Found"
        print "Found"
        #print container['Status']
        #print container['Ports']
        #print container['Id']
        if "Up" in container['Status']:
            print "Grid is Running"
        else:
            print "Grid is not Running"

    def test_can_get_grid_ip(self):
        adapter = DockerAdapter()
        container = adapter.find_container('brady/selenium-grid:latest')
        if not container:
            print "Not Found"
            return
        container_info = adapter.inspect(container['Id'])
        container = dict(container.items() + container_info.items())
        print container['NetworkSettings']['IPAddress']

    def test_can_get_nodes(self):
        adapter = DockerAdapter()
        containers = adapter.find_all_containers('brady/firefox-node:latest')
        if len(containers) == 0:
            print "Not Found"
            return

        print "Total of Firefox Nodes: " + str(len(containers))

    @unittest.skip("skipping restart")
    def test_can_restart_node(self):
        adapter = DockerAdapter()
        containers = adapter.find_all_containers('brady/firefox-node:latest')
        if len(containers) == 0:
            print "Not Found"
            return

        container = containers.pop(0)
        adapter.restart(container)

    @unittest.skip("skipping stopping nodes")
    def test_stop_all_nodes(self):
        adapter = DockerAdapter()
        containers = adapter.client.containers()
        for container in containers:
            if "node" in container['Image']:
                print "Stopping container..."
                adapter.client.stop(container['Id'])
                print "Removing container..."
                adapter.client.remove_container(container['Id'])
                #print container['Image']

    def test_start_add_node(self):
        hub = GridHub()
        ip = hub.get_ip()
        print "Grid Hub IP: " + hub.get_ip()
        # sudo docker run -d -e GRID_IP=${GRID_IP} brady/${1}-node
        adapter = DockerAdapter()
        response = adapter.client.create_container('brady/firefox-node', [], environment={"GRID_IP": ip})
        if response['Id']:
            adapter.client.start(response)

    def test_grid_start(self):
        hub = GridHub()
        hub.start()

    def test_grid_shutdown(self):
        hub = GridHub()
        hub.shutdown()




if __name__ == '__main__':
    unittest.main()

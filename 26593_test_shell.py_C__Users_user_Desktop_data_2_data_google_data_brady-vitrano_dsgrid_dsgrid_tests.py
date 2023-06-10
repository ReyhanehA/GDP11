import unittest
import os
from dsgrid import shell
from mock import patch
from dsgrid import hub

devnull = open(os.devnull, 'w')


class TestShell(unittest.TestCase):

    def setUp(self):
        pass


    @patch.object(hub.HubController, 'is_running')
    @patch.object(hub.HubController, 'start')
    def test_start(self, mock_start, mock_is_running):
        """
        Positive
        dsgrid start
        """
        mock_is_running.return_value = False
        mock_start.return_value = True
        shell.main(['start'])

    @patch.object(hub.HubController, 'is_running')
    @patch.object(hub.HubController, 'start')
    def test_start_but_container_fails(self, mock_start, mock_is_running):
        """
        Positive
        dsgrid start
        """
        mock_is_running.return_value = False
        mock_start.return_value = False
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['start'])

        self.assertEqual(cm.exception.code, 1)


    @patch.object(hub.HubController, 'is_running')
    @patch.object(hub.HubController, 'start')
    def test_start_while_running(self, mock_start, mock_is_running):
        """
        Negative: Grid is running
        dsgrid start
        """
        mock_is_running.return_value = True
        mock_start.return_value = True
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['start'])

        self.assertEqual(cm.exception.code, 1)

    @patch.object(hub.HubController, 'is_running')
    def test_shutdown(self, mock_method):
        """
        Position
        dsgrid shutdown
        """
        mock_method.return_value = True
        shell.main(['shutdown'])

    @patch.object(hub.HubController, 'is_running')
    def test_shutdown_while_not_running(self, mock_method):
        mock_method.return_value = False
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['shutdown'])
        self.assertEqual(cm.exception.code, 1)

    @patch.object(hub.HubController, 'add')
    def test_add_valid_browser(self, mock_method):
        mock_method.return_value = True
        shell.main(['nodes', 'add', 'firefox'])

    @patch.object(hub.HubController, 'add')
    def test_add_browser_with_multiple(self, mock_method):
        mock_method.return_value = True
        shell.main(['nodes', 'add', 'firefox', '2'])

    def test_add_node_invalid_browser(self):
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['nodes', 'add', 'netscape'])

        self.assertEqual(cm.exception.code, 1)

    @patch.object(hub.HubController, 'add')
    def test_add_node_but_container_fails(self, mock_method):
        mock_method.return_value = False
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['nodes', 'add', 'firefox'])
        self.assertEqual(cm.exception.code, 1)

    def test_restart_nodes(self):
        shell.main(['nodes', 'restart'])

    def test_restart_nodes_specific_browser(self):
        shell.main(['nodes', 'restart', 'firefox'])

    def test_stop_nodes(self):
        shell.main(['nodes', 'stop'])

    def test_nodes_missing_action(self):
        with patch('sys.stdout', devnull):
            with self.assertRaises(SystemExit) as cm:
                shell.main(['nodes'])

        self.assertEqual(cm.exception.code, 1)

    def test_stop_nodes_specific_browser(self):
        shell.main(['nodes', 'stop', 'firefox'])

    def test_nodes_unknown_action(self):
        with self.assertRaises(SystemExit) as cm:
            shell.main(['nodes', 'juggle'])
        self.assertEqual(cm.exception.code, 1)

    @patch.object(hub.HubController, 'is_running')
    def test_status_not_running(self, mock_method):
        mock_method.return_value = False
        #with patch('sys.stdout', devnull):
        with self.assertRaises(SystemExit) as cm:
            shell.main(['status'])
        self.assertEqual(cm.exception.code, 1)

    @patch.object(hub.HubController, 'is_running')
    def test_status_running(self, mock_method):
        mock_method.return_value = True
        shell.main(['status'])

    def test_unknown_option(self):
        with self.assertRaises(SystemExit) as cm:
            shell.main(['shake'])

        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
import unittest
from producteev import Producteev

try:
    from ConfigParser import ConfigParser
    import os
    config = ConfigParser()
    path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                         os.path.pardir))
    conf_file = open(os.path.join(path, 'tests.cfg'))
    config.readfp(conf_file)
    API_KEY = config.get('Application', 'API_KEY')
    SECRET_KEY = config.get('Application', 'SECRET_KEY')
    username = config.get('User', 'Username')
    password = config.get('User', 'Password')
except:
    import getpass
    API_KEY = raw_input('API KEY: ')
    SECRET_KEY = raw_input('SECRET KEY: ')
    username = raw_input('Username: ')
    password = getpass.getpass()


class TestProducteev(unittest.TestCase):
    """
    Test class for producteev module.
    """

    def setUp(self):
        self.client = Producteev(API_KEY, SECRET_KEY)
        self.client.login(username, password)

    def test_tasks(self):
        # Test new and get
        t1 = self.client.tasks.new('New test task')
        t2 = self.client.tasks.get(t1)
        self.assertEqual(t1, t2)

        # Test list_all
        self.assertTrue(t1, self.client.tasks.list_all())

        # Test delete
        self.assertTrue(t1.delete())

    def test_labels(self):
        # Test new and get
        dashboard_id = self.client.users.me.default_dashboard.id
        l1 = self.client.labels.new('New label', dashboard_id)
        l2 = self.client.labels.get(l1)
        self.assertEqual(l1, l2)

        # Test list
        self.assertTrue(l1, self.client.labels.list())

        # Test delete
        self.assertTrue(l2.delete())

    def test_users(self):
        me = self.client.users.me
        # Test get fullname
        fn = me.full_name
        f_l = '%s %s' % (me.firstname, me.lastname)
        self.assertEqual(fn, f_l)

        # Test sort by
        from producteev.users import SORT_BY
        ds = me.sort_by
        me.sort_by = SORT_BY[0]
        self.assertEqual(me.sort_by, SORT_BY[0])
        me.sort_by = 1
        self.assertEqual(me.sort_by, SORT_BY[1])
        me.sort_by = ds

        # Test get user
        u = self.client.users.get(me.id)
        self.assertEqual(me, u)
        u = self.client.users.get(me)
        self.assertEqual(me, u)
        u = self.client.users.get(str(me.id))
        self.assertEqual(me, u)

    def test_dashboars(self):
        # Test default dashboard
        dd = self.client.users.me.default_dashboard
        self.assertTrue(dd in self.client.dashboards.list)

        # Test new and get
        d1 = self.client.dashboards.new('New dashboard')
        d2 = self.client.dashboards.get(d1)
        self.assertEqual(d1, d2)

        # Test list
        self.assertTrue(d1 in self.client.dashboards.list)

        # Test set default dashboard
        self.client.users.me.default_dashboard = d1
        dd = self.client.users.me.default_dashboard
        self.assertEqual(dd, d1)
        self.client.users.me.default_dashboard = dd

        # Test delete
        self.assertTrue(d1.delete())

    def test_subtasks(self):
        # Test new
        t1 = self.client.tasks.new('New test task')
        st1 = self.client.subtasks.new(t1, 'New subtask')
        self.assertTrue(st1 in t1.subtasks)

        # Test delete
        self.assertTrue(st1.delete())
        self.assertTrue(t1.delete())

    def test_activities(self):
        # TODO
        pass

if __name__ == "__main__":
    unittest.main()

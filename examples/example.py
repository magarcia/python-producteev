#!/usr/bin/env python

from producteev import Producteev
from optparse import OptionParser

API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'

if __name__ == "__main__":
    # Parse options
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username",
                      help="Set username", metavar="USERNAME")
    parser.add_option("-p", "--password", dest="password",
                      help="Set password", metavar="PASSWORD")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Print status messages to stdout")

    (options, args) = parser.parse_args()

    # Make clients
    client = Producteev(API_KEY, SECRET_KEY)
    client.login(options.username, options.password)

    # Get time
    print client.get_time()

    # Get user
    user = client.users.me
    print user.timezone
    print user.default_dashboard
    print user.colleagues

    # Get task with id 9909041
    t = client.tasks.get(9909041)
    print t.title
    print t.labels
    t.title = 'New task name'

    # Get task list
    tasks = client.tasks.list_all()

    # Get dashboard list
    dashboards = client.dashboards.list
    d = dashboards[0]
    print d.title
    print d.users
    print d.tasks

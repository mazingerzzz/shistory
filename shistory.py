#!/usr/bin/env python

#
# todo : change color for root
# requirement : have a variable HISTTIMEFORMAT in your environment

import pwd
import os.path
import re
import datetime

# key = user / value = homedir
users = {}
# key = user / value = hist_pwd
hist_pwd = {}

hist_file = '/.bash_history'
hist_vrac = []

# timestamp not sorted
m_keys = []


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def list_user_homedir():
    for p in pwd.getpwall():
        if p[6] == '/bin/bash' and p[0] != 'operator':
            users[p[0]] = p[5]


def find_history():
    for k, v in users.iteritems():
        if os.path.isfile(v + hist_file):
            hist_pwd[k] = v + hist_file


def timestamp_chg():
    print "todo"


def hist_sort():
    for m_dict in hist_vrac:
        for k, v in m_dict[0].iteritems():
            m_keys.append(k)
    return m_keys.sort()


def hist_agreg():
    time_ok = False
    i = 0
    my_key = ""
    for user, path in hist_pwd.iteritems():
        try:
            f = open(path, 'r')
            for line in f:
                if time_ok is True:
                    # on affect dans la liste la command
                    hist_vrac.append([{my_key: [user, line]}])
                    i += 1
                    time_ok = False
                if re.search('^#10*[0-9]', line) and time_ok is False:
                    # on ajoute la key du dict
                    my_key = line.replace('#', '')
                    my_key = my_key.replace('\n', '')
                    time_ok = True
                else:
                    pass
            f.closed
        except IOError:
            pass


def colors_chg():
    n = 0
    c = 0
    for i in m_keys:
        for n in range(len(m_keys)):
            # timestamp to string
            current_key = hist_vrac[n][0].keys()
            current_key = ''.join(map(str, current_key))
            if current_key == i:
                c += 1
                current_user = hist_vrac[n][0][current_key][0]
                current_cmd = hist_vrac[n][0][current_key][1]
                print "",
                print bcolors.BLUE + str(c) + bcolors.ENDC,
                print "",
                print bcolors.GREEN + current_user + bcolors.ENDC,
                print bcolors.YELLOW + (
                    datetime.datetime.fromtimestamp(
                        int(current_key)
                    ).strftime('%Y-%m-%d %H:%M:%S')
                ) + bcolors.ENDC,
                print bcolors.GREEN + ">" + bcolors.ENDC,
                print bcolors.RED + current_cmd + bcolors.ENDC,
                pass


list_user_homedir()
find_history()
hist_agreg()
hist_sort()
colors_chg()

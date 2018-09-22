#!/usr/bin/env python2.7

#
# todo : change color for root
# requirement : have a variable HISTTIMEFORMAT in your environment

import datetime
import os.path
import pwd
import re
import cProfile

# key = user / value = homedir
users = {}
# key = user / value = hist_path
hist_pwd = {}

hist_file = '/.bash_history'

# [{unixtimestamp: [user, command]

hist_vrac = []

# timestamp list
m_keys = []
users_blacklist = ['operator']


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
        if p[6] == '/bin/bash' and p[0] not in users_blacklist:
            users[p[0]] = p[5]


def find_history():
    for k, v in users.iteritems():
        if os.path.isfile(v + hist_file):
            hist_pwd[k] = v + hist_file


def timestamp_chg(my_date):
    t_stamp = (
            datetime.datetime.fromtimestamp(
                int(my_date)
            ).strftime('%Y-%m-%d %H:%M:%S')
    )
    return t_stamp


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


def left_space(c):
    l_space_nbr = 0
    len_c = 0
    nbr_line = 0
    nbr_line = len(str(len(m_keys)))
    len_c = len(str(c))
    if c == 1:
        l_space_nbr = nbr_line - len_c + 1
        return multi_space(l_space_nbr)

    l_space_nbr = nbr_line - len_c
    return multi_space(l_space_nbr)


def right_space(user):
    r_space_nbr = 0
    r_space_nbr = max_len_user() - len(user)
    return multi_space(r_space_nbr)


def max_len_user():
    user = []
    maxi = ""
    user_maxi = []
    for k, v in users.iteritems():
        user.append([k])
    user_maxi = max(user)
    maxi = len(''.join(map(str, user_maxi)))
    return maxi


def multi_space(space_nbr):
    space = ""
    for i in range(space_nbr):
        space += " "
    if space_nbr == 0:
        space = ""
    return space


def result():
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
                print left_space(c),
                print bcolors.BLUE + str(c) + bcolors.ENDC,
                print bcolors.GREEN + right_space(current_user) + bcolors.ENDC,
                print bcolors.GREEN + current_user + bcolors.ENDC,
                print bcolors.YELLOW + timestamp_chg(current_key) + bcolors.ENDC,
                print bcolors.GREEN + ">" + bcolors.ENDC,
                print bcolors.RED + current_cmd + bcolors.ENDC,
                hist_vrac[n][0]['42'] = hist_vrac[n][0][current_key]


def main():
    list_user_homedir()
    find_history()
    hist_agreg()
    hist_sort()
    result()


if __name__ == "__main__":
    main()

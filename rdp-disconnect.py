# USAGE: python rdp-disconnect.py -u kadir.malak -s 192.168.0.10 192.168.0.11 somehostname1 somehostname2

from subprocess import check_output, STDOUT
import argparse

def rdp_session_id(server, username):
    output = check_output('qwinsta /server:%s %s' % (server, username), stderr=STDOUT).decode('latin1')
    if 'No session exists' in output:
        return -1
    lines = [line.split() for line in output.split('\r\n')]
    if lines[1][0] == username:
        lines[1] = [''] + lines[1]
    info = dict(zip(lines[0], lines[1]))
    return int(info['ID'])

def rdp_reset_session(server, session_id):
    return check_output('rwinsta /server:%s %d' % (server, session_id), stderr=STDOUT).decode('latin1')

def rdp_reset_sessions(servers, username):
    sessions = [(s, rdp_session_id(s, username)) for s in servers]
    valid_sessions = [p for p in sessions if p[1] > 0]
    for p in valid_sessions:
        rdp_reset_session(p[0], p[1])
    return len(valid_sessions)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-s', '--servers', nargs='+', required=True)
    args = parser.parse_args()

    print('username: %s' % args.username)
    print('servers: %s' % args.servers)

    count = rdp_reset_sessions(args.servers, args.username)
    print('%d sessions removed' % count)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, os, argparse, textwrap

##############################get_terminal_size##########################################
import shlex
import struct
import platform
import subprocess

g_cowsays_path = "/usr/share/cowsay/cows/"

def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        # print(default)
        tuple_xy = (80, 25)      # default value
    return tuple_xy
 
 
def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass
 

def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass
 
 
def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

################################Cow builder##########################################

def cow_parse(cow_path, tail, eyes, tongue):
    """Read the .cow file."""
    perl_cow = [
        unicode(
            line
            .replace("$thoughts", tail)
            .replace("${thoughts}", tail)
            .replace("$eyes", eyes)
            .replace("${eyes}", eyes)
            .replace("$tongue", tongue)
            .replace("${tongue}", tongue)
            .replace("\\\\", "\\")
            .replace("\\$", "$").replace("\\@", "@")
        )
        for line in open(cow_path)
    ]
    the_cow = ""
    cow_line = False
    for line in perl_cow:
        if "EOC" not in line and cow_line:
            the_cow += line
        if "the_cow" in line:
            cow_line = True
    return the_cow.rstrip()

def build_balloon(cols, msg):
    # handle '\n' in message and wrap message
    msg_lines = msg.split('\\n')
    msg_lines_wrap = []
    for line in msg_lines:
        msg_lines_wrap.append(textwrap.fill(line,width=cols,expand_tabs=False,break_on_hyphens=False))

    msg_string = "\n".join(msg_lines_wrap)
    msg_lines = msg_string.splitlines()

    # get border length
    max_str_len = len(max(msg_lines, key=len))
    border_len = max_str_len + 2
    balloon_lines = []

    # first line
    balloon_lines.append(" " +  "_"*border_len)
    strFormat = "{{0}} {{1:<{str_len}}} {{2}}".format(str_len=max_str_len)

    # massge text with borders. 
    if len(msg_lines) == 1:
        balloon_lines.append(strFormat.format("<", msg_lines[0], ">"))
    else:
        balloon_lines.append(strFormat.format("/", msg_lines[0], "\\"))
        for line in msg_lines[1:-1]:
            balloon_lines.append(strFormat.format("|", line, "|"))

        balloon_lines.append(strFormat.format("\\", msg_lines[-1], "/"))
    #end of balloon
    balloon_lines.append(" " +  "-"*border_len)
    return balloon_lines

def find_cow(name):
    # file with path 
    if name.endswith(".cow") and os.path.exists(name):
        return name

    # get cow from cowsays
    name = name+'.cow'
    env_path = os.environ.get('COWSPATH')
    if (not env_path) or (not os.path.exists(g_cowsays_path)):
        print("Please install 'cowsays' or '-f' to set cow file path")
        sys.exit()

    for f in os.listdir(g_cowsays_path):
        if f == name:
            return os.path.join(g_cowsays_path, f)

    # get cow files from env
    for f in os.listdir(env_path):
        if f == name:
            return os.path.join(env_path, f)
    return None

def get_cow(cow_file, tail, eyes, tongue):
    cow = find_cow(cow_file)
    if not cow:
        print("Could not find {} cowfile!".format(cow_file))
        sys.exit()

    # read line by line into list and replace face items
    file_lines = [ line.replace("$thoughts", tail)
                        .replace("${thoughts}", tail)
                        .replace("$eyes", eyes)
                        .replace("${eyes}", eyes)
                        .replace("$tongue", tongue)
                        .replace("${tongue}", tongue)
                        .replace("\\@", "@")
                        .replace("\\$", "$")
                        .replace("\\\\", "\\")
                         for line in open(cow) ]

    cow_text = ""
    the_cow = False
    for line in file_lines:
        if "EOC" not in line and the_cow:
            cow_text += line
        if "the_cow" in line:
            the_cow = True
    return cow_text

def list_cowfiles():
    cows = []
    # get cow from cowsays
    for f in os.listdir(g_cowsays_path):
        if f.endswith(".cow"):
            cows.append(f.replace(".cow", ""))

    # get cow files from env
    env_path = os.environ.get('COWSPATH')
    if env_path:
        for f in os.listdir(env_path):
            if f.endswith(".cow"):
                cows.append(f.replace(".cow", ""))
    print(" ".join(cows))
    sys.exit()

def list_cowfiles2():
    cows = ["Cows in: '{}'\n".format(g_cowsays_path)] 
    # get cow from cowsays
    for f in os.listdir(g_cowsays_path):
        if f.endswith(".cow"):
            cows.append(f.replace(".cow", ""))

    print(" ".join(cows))
    # get cow files from env
    env_path = os.environ.get('COWSPATH')
    if env_path:
        cows = ["\nCows in: '{}'\n".format(env_path)] 
        for f in os.listdir(env_path):
            if f.endswith(".cow"):
                cows.append(f.replace(".cow", ""))
        print(" ".join(cows))
    
    sys.exit()

def init_argParser():
    parser = argparse.ArgumentParser(prog='cowquotes.py', description='cowsays with online quotes! inspired by cowsays.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", action="store_true", dest="borg", help="eyes are '==' (borg)")
    group.add_argument("-d", action="store_true", dest="dead", help="eyes are 'xx' and tongue is 'U ' (dead)")
    group.add_argument("-g", action="store_true", dest="greedy", help="eyes are '$$' (greedy)")
    group.add_argument("-p", action="store_true", dest="paranoid", help="eyes are '@@' (paranoid)")
    group.add_argument("-s", action="store_true", dest="stoned", help="eyes are '**' and tongue is 'U ' (stoned)")
    group.add_argument("-t", action="store_true", dest="tired", help="eyes are '--' (tired)")
    group.add_argument("-w", action="store_true", dest="wired", help="eyes are 'OO' (wired)")
    group.add_argument("-y", action="store_true", dest="young", help="eyes are '..' (young)")
    parser.add_argument("-l", action="store_true", dest="listcows", help="list cows")
    parser.add_argument("-f", default="default", dest="cowfile", help="name of the cow file to show")
    parser.add_argument("-W", default=0, type=int, dest="wrapcolumn", help=("max column size of balloon"))
    parser.add_argument("-e", default="oo", dest="eyes", help="two characters for eyes")
    parser.add_argument("-T", default="  ", dest="tongue", help="two characters for tongue")
    parser.add_argument("-m", dest="message", help="message")
    return parser

def get_facial(args):

    eyes = "oo"
    tongue = "  "
    if args.borg:
        eyes = "=="
    elif args.dead:
        eyes = "xx"; tongue = "U "
    elif args.greedy:
        eyes = "$$"
    elif args.paranoid:
        eyes = "@@"
    elif args.stoned:
        eyes = "**"; tongue = "U "
    elif args.tired:
        eyes = "--"
    elif args.wired:
        eyes = "OO"
    elif args.young:
        eyes = ".."
    else:
        eyes = args.eyes
        tongue = args.tongue

    return eyes, tongue

###############################Online Quotes#########################################
import json, random, requests
import re
from requests.exceptions import ConnectionError 

def quotes_forismatic():
    '''
    http://forismatic.com/en/api/ 
    '''
    # key=<integer> - numeric key, which influences the choice of quotation, the maximum length is 6 characters
    # http://api.forismatic.com/api/1.0/?method=getQuote&key=3&format=json&lang=en
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&key={}&format=json&lang=en".format(random.randint(0,999999))
    # ValueError: Invalid \escape
    regex = re.compile(r'\\(?![/u"])')
    try:
        response = requests.get(url)
    except ConnectionError:
        return "Moooo! \\n Get online quote error: ConnectionError \\n"

    if response.status_code != requests.codes.ok:
        return "Moooo! \\n Get online quote error: {} \\n".format(response.status_code)

    text = regex.sub(r"\\\\", response.text)
    quote_json = json.loads(text)
    quote = quote_json["quoteText"]+"\\n "
    author = quote_json["quoteAuthor"]
    if author is not "":
        quote = quote + "\\n<< " + author +" >> from Forismatic\\n"
    return quote

def quotes_forbes():
    '''
    https://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=1
    '''
    url = "https://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=1"
    try:
        response = requests.get(url)
    except ConnectionError:
        return "Moooo! \\n Get online quote error: ConnectionError \\n"

    if response.status_code != requests.codes.ok:
        return "Moooo! \\n Get online quote error: {} \\n".format(response.status_code)

    forbes = json.loads(response.text)
    quote = forbes["thought"]["quote"]+"\\n "
    author = forbes["thought"]["thoughtAuthor"]["name"]
    if author is not "":
        quote = quote + "\\n<< " + author +" >> from Forbes\\n"
    return quote

def get_quotes():
    seed = random.randint(0,100)
    if seed < 90:
        return quotes_forismatic()
    else:
        return quotes_forbes()


###############################Main##################################################
if __name__=='__main__':

    ps = init_argParser()
    args = ps.parse_args()

    # list cow models only
    if args.listcows:
        list_cowfiles()

    # character length of messages
    if args.wrapcolumn == 0:
        width, height = get_terminal_size()
        cols = width/3
        cols = 40 if cols < 40 else cols
    else:
        cols = args.wrapcolumn

    # parsing face
    eyes, tongue = get_facial(args)
    
    # if no message, get online quotes 
    if args.message:
        balloon = build_balloon(cols, args.message)
    else:
        online_quotes  = get_quotes()
        balloon = build_balloon(cols,online_quotes)

    # construct the cow
    cow = get_cow(args.cowfile,"\\",eyes,tongue)

    # print out the message and cow
    for x in balloon:
        print(x)
    print(cow)
    sys.exit()


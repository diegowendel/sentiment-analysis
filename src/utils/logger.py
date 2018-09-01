'''
    Logger - Classe utilitária para printar mensagens na tela
'''

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger(object):

    def ok(message):
        print(colors.OKBLUE + message + colors.ENDC)

    def success(message):
        print(colors.OKGREEN + message + colors.ENDC)

    def warn(message):
        print(colors.WARNING + message + colors.ENDC)

    def error(message):
        print(colors.FAIL + colors.BOLD + message + colors.ENDC)

    def log(message):
        print('Log: ' + message)
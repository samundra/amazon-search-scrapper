class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def bred(message):
        print bcolors.FAIL+message+bcolors.ENDC
        return " "

    @staticmethod
    def bgreen(message):
        print bcolors.OKGREEN+message+bcolors.ENDC
        return " "
import configparser
import logging
from os.path import exists

config = configparser.ConfigParser()

def create_default_config(filename='config.ini'):

    config['SECRETS'] = {'DiscordToken':'put-a-token-here',
                         "OpenAIToken":"put-another-one-here"}
    config['OPTIONS'] = {'WhisperMode':'local-or-online',
                         "WhisperModel":"medium"}

    with open(filename, 'w') as configfile:
        config.write(configfile)


def check_existance(filename="config.ini"):
    if exists(filename):
        return True
    else:
        return False


#            logging.info("Config created, exiting.")
#            sys.exit()

def read_config(filename='config.ini'):
    config.read(filename)
    return config


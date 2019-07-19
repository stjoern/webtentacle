import argparse
import sys
from keyrings.cryptfile.cryptfile import CryptFileKeyring
import os


class Crypt(object):
    
    def __init__(self):
        self.path = "/root/.local/share/webtentacle_keyring"
        self.mother_service='?'
        self.kr = CryptFileKeyring()
        self.kr.keyring_key='?'
        parser = argparse.ArgumentParser(
            description="Decrypt the system file",
            usage='''crypt decrypt --username <username>
            crypt encrypt --username <username> --password <password> 
            
The most commonly used decrypt commands are:
    crypt decrypt --username admin, returns password           
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()
            
    def decrypt(self):
        try:
            parser = argparse.ArgumentParser(
                description="decrypt service usernames's password")
            parser.add_argument('--username', '-u')
            args = parser.parse_args(sys.argv[2:])
           
            # invoke the keyring
            print(self.kr.get_password(self.mother_service, args.username), end='')
        except Exception as msg:
            print("Error in keyring decryption, {}".format(str(msg)))
            sys.exit(2)
        
    def encrypt(self):
        try:
            parser = argparse.ArgumentParser(
                description="encrypt service username's passowrd"
            )
            parser.add_argument('--username','-u')
            parser.add_argument('--password','-p')
            args = parser.parse_args(sys.argv[2:])
            self.kr.set_password(self.mother_service, args.username, args.password)
            return 0
        except Exception as msg:
            print("Error in keyring encryption, {}".format(str(msg)))
            sys.exit(2)
        
if __name__ == '__main__':
    Crypt()
        
import crypt
import random

class Utils:
    @staticmethod
    def random_passwd():
        """Generate a 8 chars long passwd"""
        li = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890./"
        
        passwd = str()
        for i in range(8):
            passwd = passwd + str(random.choice(li))
        
        return passwd
          
    @staticmethod
    def encrypt_passwd(passwd=None):
        """Encrypt a passorwd using a random 2 chars salt"""
        li = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890./"

        if passwd is None:
            passwd = self.random_passwd()

        salt = str()
        for i in range(2):
            salt = salt + str(random.choice(li))
        
        return (passwd, crypt.crypt(passwd, salt))
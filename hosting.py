#!/usr/bin/env python2.5
# vim: tabstop=4 expandtab shiftwidth=4
import sys
import os
import subprocess
import shutil
import crypt
import random
from optparse import OptionParser
import getpass

# Round Cube webmail user creation
#CREATE USER 'roundcube'@ 'localhost' IDENTIFIED BY '****************';
#GRANT USAGE ON * . * TO 'roundcube'@ 'localhost' IDENTIFIED BY '****************' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;
#CREATE DATABASE `roundcube` ;
#GRANT ALL PRIVILEGES ON `roundcube` . * TO 'roundcube'@ 'localhost';

APPNAME="hosting.py"
APPVERSION="0.1"

BASEDIR = "/home"
SKEL = "/etc/skel-www"
AVAILABLE = "/etc/apache2/sites-available"
#ENABLED = "/etc/apache2/sites-enabled"
SHELL = "/bin/false"
DOMAIN = "lapin-blanc.net"
ADMIN = "contact@lapin-blanc.net"
VHOST = """<VirtualHost *>
        ServerName %(domain)s
        ServerAdmin %(email)s
        
        ServerSignature Off

        DocumentRoot %(document_root)s
        <Directory %(home)s>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
        </Directory>

        ErrorLog %(logs)s/error.log
        LogLevel warn
        CustomLog %(logs)s/access.log combined
</VirtualHost>"""


class Mysql:
    """Manage MySQL accounts and databases"""
    def __init__(self, username):
        self.username = username
    
    def add(self, password=None):
        pass
    
    def modify(self, password=None):
        pass
    
    def delete(self):
        pass


class Site:
    """Manage Apache virtuals hosts"""
    def __init__(self, name):
        self.name = name

    def add(self, email=None, domain=None):
        """Create a vhost"""
        if email is None:
            email = ADMIN
        if domain is None:
            domain = "%s.%s" % (self.name, DOMAIN)
        home = os.path.join(BASEDIR, self.name)
        document_root = os.path.join(home, "public_html")
        logs = os.path.join(home, "logs")
        vhost = VHOST % {"domain": domain, "email": email, "home": home,\
            "document_root": document_root, "logs": logs}
        file = os.path.join(AVAILABLE, self.name)
        f = open(file, "w")
        f.write(vhost)
        f.close()
        self.enable()

    def enable(self):
        """Enable a vhost"""
        subprocess.check_call(["a2ensite", self.name])

    def disable(self):
        """Disable a vhost"""
        subprocess.check_call(["a2dissite", self.name])

    def modify(self, email=None, domain=None):
        """Modify a vhost"""
        self.delete()
        self.add(email, domain)
    
    def delete(self):
        """Delete a vhost"""
        self.desable()
        file = os.path.join(AVAILABLE, self.name)
        os.unlink(file)


class Account:
    """Manage UNIX accounts"""
    def __init__(self, username):
        self.username = username

    def add(self, password, shell=None, email=None, domain=None):
        """Add an account"""

        comment = "Web account for "
        #sep = False
        #if email is not None:
        #    comment = comment + email
        #    sep = True
        #if domain is not None:
        #    if sep:
        #        comment = comment + " - "
        #    comment = comment + domain

        comment = comment + self.username
        
        if email is not None:
            comment = comment + "(%s" % email
        if domain is not None:
            comment = comment + " - %s)" % domain
        elif email is not None:
            comment = comment + ")"
        
        password = Main.password(password)
        if shell is None:
            shell = SHELL
        # We don't use -b (--base-dir) because it seems to have a blocking bug in the etch's useradd
        subprocess.check_call(["useradd","-c", comment, "-m", "-d", os.path.join(BASEDIR, self.username),\
        	"-k", SKEL, "-s", shell, "-p", password[1],  self.username])
        return password[0]

    def change_password(self, password=None):
        """Change an account's password"""
        password = self.password(password)
        subprocess.check_call(["usermod", "-p", password[1], self.username])
        return password[0]

    def change_shell(self, shell):
        """Change an account's shell"""
        subprocess.check_call(["usermod", "-s", shell, self.username])

    def modify(self, password=None, shell=None):
        """Modify an account"""
        if password is not None:
            self.change_password(password)
        if shell is not None:
            self.change_shell(shell)

    def delete(self, delete_data=False):
        """Delete an account"""
        subprocess.check_call(["userdel", self.username])
        
        if delete_data:
            shutil.rmtree("%s/%s" % (BASEDIR, self.username))


class Main:
    """Main program"""
    def __init__(self):
        parser = OptionParser(usage="""%prog command username
Commands:
	add		Add an account
	del		Delete an account
	mod		Modify account""", version="%prog " + APPVERSION)
        parser.add_option("-p", "--password", action="store_true",\
            dest="password", help="ask for password")
        parser.add_option("-b", "--batch", action="store_true",\
            default=False, dest="batch", help="batch mode")  
        parser.add_option("-s", "--shell", dest="shell",\
            help="use SHELL", metavar="SHELL")
        parser.add_option("-e", "--email", dest="email",\
            help="set EMAIL", metavar="EMAIL")
        parser.add_option("-n", "--domain-name", dest="domain",\
            help="set default DOMAIN", metavar="DOMAIN")
 
        (options, args) = parser.parse_args()
        if len(args) is not 2:
            parser.error("Require two arguments")
        command = args[0]
        username = args[1]
        a = Account(username)
        s = Site(username)
        if command == "add":
            if options.password:
                password = self.getpass(options.batch)
            else:
                password = None
            pwd = a.add(password, options.shell, options.email, options.domain)
            s.add(options.email, options.domain)
            print "Login: %s" % username
            print "Password: %s" % pwd
            print "Domain: %s.%s" % (username, DOMAIN)
        elif command == "mod":
            if options.password:
                password = self.getpass(options.batch)
            else:
                password = None
            a.modify(password, options.shell)
            s.modify(options.email, options.domain)
        elif command == "del":
            a.delete()
            s.delete()
        else:
            parser.error("Unknow command")
        
    def getpass(batch=False):
        """Get a password"""
        if batch:
            return raw_input("Password:")
        try:
            return getpass.getpass()
        except:
            print "Error: invalid argument"
            print "Try using --batch"
            sys.exit(2)
    
    @staticmethod
    def password(password=None):
        """Encrypt a password using a random 2 chars salt.
        If the password is None generate a 8 chars long."""
        li = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890./"

        if password is None:
            password = str()
            for i in range(8):
                password = password + str(random.choice(li))

        salt = str()
        for i in range(2):
            salt = salt + str(random.choice(li))
        
        return (password, crypt.crypt(password, salt))


if __name__ == "__main__":
    Main()

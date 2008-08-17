#!/usr/bin/env python2.5
# vim: set fileencoding=utf-8 :
# Copyright (C) 2008 Kévin Dunglas <dunglas@gmail.com>
#
# Authors:
#  Kévin Dunglas
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA

import sys
from optparse import OptionParser
import getpass
from hosting.Unix import Unix
from hosting.Mysql import Mysql
from hosting.Apache import Apache
from hosting.Utils import Utils

APPNAME    = "hosting.py"
APPVERSION = "0.2"

MYSQL_HOST   = "localhost"
MYSQL_USER   = "root"
MYSQL_PASSWD = ""

BASEDIR      = "/home"
SKEL         = "/etc/skel-www"
AVAILABLE    = "/etc/apache2/sites-available"
#ENABLED     = "/etc/apache2/sites-enabled"
SHELL        = "/bin/false"
DOMAIN       = "lapin-blanc.net"
ADMIN        = "contact@lapin-blanc.net"
VHOST        = """<VirtualHost *>
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


class Main:
    """Main program"""
    def __init__(self):
        parser = OptionParser(usage="""%prog command username
Commands:
	add		Add an account
	del		Delete an account
	mod		Modify account""", version="%prog " + APPVERSION)
        parser.add_option("-p", "--passwd", action="store_true",\
            dest="passwd", help="ask for passwd")
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
        u = Unix(username, BASEDIR, SKEL, SHELL)
        a = Apache(username, VHOST, AVAILABLE, BASEDIR, ADMIN, DOMAIN)
        m = Mysql(username, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD)
        
        if command == "add":
            print "Add..."
            if options.passwd:
                passwd = self.getpass(options.batch)
            else:
                passwd = Utils.random_passwd()

            u.add(passwd, options.shell, options.email, options.domain)
            a.add(options.email, options.domain)
            m.add(passwd)
            
        elif command == "mod":
            if options.passwd:
                passwd = self.getpass(options.batch)
            else:
                passwd = Utils.random_passwd()
            
            u.modify(passwd, options.shell)
            a.modify(options.email, options.domain)
            m.modify(passwd)
        elif command == "del":
            u.delete()
            a.delete()
            m.delete()
        else:
            parser.error("Unknow command")
        
    def getpass(self, batch=False):
        """Get a password"""
        if batch:
            return raw_input("passwd:")
        try:
            return getpass.getpass()
        except:
            print "Error: invalid argument"
            print "Try using --batch"
            sys.exit(2)

if __name__ == "__main__":
    Main()

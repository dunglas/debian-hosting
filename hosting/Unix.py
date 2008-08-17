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

import os
import subprocess
import shutil
from Utils import Utils

class Unix:
    """Manage UNIX accounts"""
    def __init__(self, username, basedir, skel, shell):
        self.__username = username
        self.__basedir = basedir
        self.__skel = skel
        self.__shell = shell

    def add(self, passwd, shell=None, email=None, domain=None):
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

        comment = comment + self.__username
        
        if email is not None:
            comment = comment + "(%s" % email
        if domain is not None:
            comment = comment + " - %s)" % domain
        elif email is not None:
            comment = comment + ")"
        
        enc_passwd = Utils.encrypt_passwd(passwd)
        if shell is None:
            shell = self.__shell
        # We don't use -b (--base-dir) because it seems to have a blocking bug in the etch's useradd
        subprocess.check_call(["useradd","-c", comment, "-m", "-d", os.path.join(self.__basedir, self.__username),\
                "-k", self.__skel, "-s", shell, "-p", passwd[1],  self.__username])
        
        print "UNIX account added."
        print "Username: %s" % self.__username
        print "Password: %s" % passwd

    def __change_passwd(self, passwd=None):
        """Change an account's passwd"""
        passwd = self.passwd(passwd)
        subprocess.check_call(["usermod", "-p", passwd[1], self.__username])
        
    def __change_shell(self, shell):
        """Change an account's shell"""
        subprocess.check_call(["usermod", "-s", shell, self.__username])

    def modify(self, passwd=None, shell=None):
        """Modify an account"""
        if passwd is not None:
            self.__change_passwd(passwd)
        if shell is not None:
            self.__change_shell(shell)
        
        print "UNIX account modified."

    def delete(self, delete_data=False):
        """Delete an account"""
        subprocess.check_call(["userdel", self.__username])
        
        if delete_data:
            shutil.rmtree("%s/%s" % (BASEDIR, self.__username))
        
        print "UNIX account deleted."
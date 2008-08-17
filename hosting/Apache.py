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

class Apache:
    """Manage Apache virtuals hosts"""
    def __init__(self, name, vhost, available, basedir, admin, domain):
        self.__name = name
        self.__vhost = vhost
        self.__domain = domain
        self.__available = available
        self.__basedir = basedir
        self.__admin = admin

    def add(self, email=None, domain=None):
        """Create a vhost"""
        if email is None:
            email = self.__admin
        if domain is None:
            domain = "%s.%s" % (self.__name, self.__domain)
        home = os.path.join(self.__basedir, self.__name)
        document_root = os.path.join(home, "public_html")
        logs = os.path.join(home, "logs")
        vhost = self.__vhost % {"domain": domain, "email": email, "home": home,\
            "document_root": document_root, "logs": logs}
        file = os.path.join(self.__available, self.__name)
        f = open(file, "w")
        f.write(vhost)
        f.close()
        print "Apache virtual host added."
        print "URL:     %s" % domain
        
        self.__enable()

    def __enable(self):
        """Enable a vhost"""
        subprocess.check_call(["a2ensite", self.__name])

    def __disable(self):
        """Disable a vhost"""
        subprocess.check_call(["a2dissite", self.__name])

    def modify(self, email=None, domain=None):
        """Modify a vhost"""
        self.delete()
        self.add(email, domain)
        
        print "Apache virtual host modified."
    
    def delete(self):
        """Delete a vhost"""
        self.__disable()
        file = os.path.join(self.__available, self.__name)
        os.unlink(file)
        
        print "Apache virtual host deleted."
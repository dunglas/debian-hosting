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

import MySQLdb

class Mysql:
    """Manage MySQL accounts and databases"""
    def __init__(self, username, host, user, passwd):
        self.__username = username
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__db = MySQLdb.connect(host=self.__host, user=self.__user, passwd=self.__passwd);
        self.__cursor = self.__db.cursor()
    
    def add(self, password):
        database = self.__username.replace(".", "_")
        query = "CREATE DATABASE `%s`;" % database
        self.__cursor.execute(query)
        
        #if password is None:
        #    query = "CREATE USER '%s'@'%s';" % (self.username, self.__host)
        #else:
        #    query = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';" % (self.username, self.__host, password)
        query = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';" % (self.__username, self.__host, password)
        self.__cursor.execute(query)
        
        query = "GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'%s' WITH GRANT OPTION;" % (database, self.__username, self.__host)
        self.__cursor.execute(query)
        
        query = "FLUSH PRIVILEGES;"
        self.__cursor.execute(query)
        
        print "MySQL account added."
        print "Username: %s" % self.__username
        print "Password: %s" % password
        print "Database: %s" % database
        print "Host:     %s" % self.__host
    
    def modify(self, password=None):
        query = "SET PASSWORD FOR '%s'@'%s' = PASSWORD('%s');" % (self.__username, self.__host, password)
        self.__cursor.execute(query)
        
        print "MySQL account modified."
    
    def delete(self, delete_data=False):
         query = "DROP USER '%s'@'%s';" % (self.__username, self.__host)
         self.__cursor.execute(query)
         
         if delete_data:
             query = "DROP DATABASE `%s`;" % self.__username
             self.__cursor.execute(query)
         
         query = "FLUSH PRIVILEGES;"
         self.__cursor.execute(query)
         
         print "MySQL account deleted."
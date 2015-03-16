# hosting.py #

_hosting.py_ is a web server account manager for [Debian GNU/Linux](http://www.debian.org) and derivatives, such as [Ubuntu Linux](http://www.ubuntu.com).

This is a command line tool designed to easily create, modify and delete web accounts.
It includes support for **UNIX accounts, [MySQL](http://www.mysql.com) databases and privileges, and [Apache](http://httpd.apache.org) virtual hosts**.

_hosting.py_ is wrote in [Python](http://www.python.org) by [Kévin Dunglas](http://lapin-blanc.net).


## Summary ##

_hosting.py_ is designed for small web hosting services like privates shared hosts or big websites with many subdomains.


## Install ##

_hosting.py_ need Debian etch or Ubuntu and Python 2.5 to work.
Get the source via SVN :
`svn checkout http://debian-hosting.googlecode.com/svn/trunk/ debian-hosting-read-only`

Create the base skeleton for web accounts :
`mkdir /etc/skel-www/`
`mkdir /etc/skel-www/logs/`
`mkdir /etc/skel-www/public_html/`

You can add any file in `/etc/skel-www/` (by example an `index.html` file in `public_html/`). They will be copied in each home directory created with _hosting.py_.

Adjust the configuration by editing variables in the head of the _hosting.py_ file. Default values are good excepts for MySQL related settings.

It's done !

## Usage ##

hosting.py command username
Commands:
> add             Add an account
> del             Delete an account
> mod             Modify account

Options:
> --version             show program's version number and exit
> -h, --help            show this help message and exit
> -p, --passwd          ask for passwd
> -b, --batch           batch mode
> -s SHELL, --shell=SHELL
> > use SHELL

> -e EMAIL, --email=EMAIL
> > set EMAIL

> -n DOMAIN, --domain-name=DOMAIN
> > set default DOMAIN

Type `python hosting.py --help` to get more informations.
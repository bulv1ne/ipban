ipban
=====

ipban is a django app that keeps spammers away in an easy way.


Install
-------

* Clone this repository into your django project.
* Add 'ipban' to the INSTALLED_APPS in settings.py
* Sync your database with ./manage.py syncdb
* Add @ipban to any view you want to secure

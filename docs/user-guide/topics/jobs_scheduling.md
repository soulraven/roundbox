Jobs Scheduling
===============

Documentation on creating/using jobs in RoundBox

Creating jobs works much like management commands work in RoundBox.

Setup
-----

Run:

```bash
$ python manage.py create_jobs <roundbox_application>
```

to make a ``jobs`` directory inside an application. The ``jobs`` directory will have the following tree:

    jobs
    ├── daily
    │   └── __init__.py
    ├── hourly
    │   └── __init__.py
    ├── monthly
    │   └── __init__.py
    ├── weekly
    │   └── __init__.py
    ├── yearly
    │   └── __init__.py
    ├── __init__.py
    └── sample.py

Create a job
------------

A job is a Python script with a mandatory ``BaseJob`` class which extends from
``MinutelyJob``, ``QuarterHourlyJob``, ``HourlyJob``, ``DailyJob``, ``WeeklyJob``, ``MonthlyJob`` or ``Yearly``.
It has one method that must be implemented called ``execute``,
which is called when the job is run.
The directories ``hourly``, ``daily``, ``monthly``, ``weekly`` and ``yearly`` are used only to for organisation purpose.

!!! Note
    If you want to use ``QuarterHourlyJob`` or ``Minutely`` job, create python package with name ``quarter_hourly``
    or ``minutely`` respectively (similar to ``hourly`` or ``daily`` package).

To create your first job you can start copying ``sample.py``.
Remember to replace ``BaseJob`` with ``MinutelyJob``, ``QuarterHourlyJob``, ``HourlyJob``, ``DailyJob``, ``WeeklyJob``,
``MonthlyJob`` or ``Yearly``.

Note that each job should be in a new python script (within respective directory) and the class implementing the cron should be named ``Job``. Also, ``__init__.py`` file is not used for identifying jobs.

Run a job
---------

The following commands are related to jobs:

* ``create_jobs``, create the directory structure for jobs
* ``runjob``, run a single job
* ``runjobs``, run all hourly/daily/weekly/monthly jobs

Use "runjob(s) -l" to list all jobs recognized.

Jobs do not run automatically!
You must either run a job manually specifying the exact time on
which the command is to be run, or use crontab:

```shell
@hourly /path/to/my/project/manage.py runjobs hourly

@daily /path/to/my/project/manage.py runjobs daily

@weekly /path/to/my/project/manage.py runjobs weekly

@monthly /path/to/my/project/manage.py runjobs monthly
```

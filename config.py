'''

### backup_timings

backup_timings is assigned to each account in accounts.py if no 'backup_timings'
is found. This allows for quick, global backup management and account-specific
settings

interval     int Number of hours between each backup
expire_after int Number of hours to keep snapshots for

'''

iStopLogsAtLevel = 9  # int Escalating log level. 0 = NONE, 9 = ALL
bPrintLogMsgs = True
sLogFilename = 'logfile'
bPrintToLogFile = False

backup_timings = {
    'daily': {
        'interval': 24,
        'expire_after': (24 * 7)
    },
    'weekly': {
        'interval': (24 * 7),
        'expire_after': (24 * 7 * 4)
    },
    'monthly': {
        'interval': (24 * 7 * 4),
        'expire_after': (24 * 7 * 52)
    }
}

'''

### aws

'accountname' string UNIQUE custom reference for the account
    'key'     string AWS IAM user account key ID
    'secret'  string AWS IAM user account secret ID

'''

aws = {
    'dev' : {
        'key'       : 'abcd',
        'secret'    : '1234',
        # # You can specify account-specific timings here aswell. This are pre-populated by Config.py
        #'backup_timings' : {
        #    'daily' : {
        #        'interval'     : 24, # Set the interval to 0 to disable this backup type
        #        'expire_after' : (24 * 7)
        #    },
        #}
    },
    #'dev2' : {
    #    'key'       : 'abcd',
    #    'secret'    : '1234'
    #},
}

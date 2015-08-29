#!/usr/bin/env python

import accounts
import config
import datetime

from boto import ec2

'''
This script loops through each AWS account found in accounts.py and creates a
snapshot of every instance, on every region.

Uses the boto library <https://github.com/boto/boto>

@author Peter McConnell <peter.mcconnell@rehabstudio.com>
'''

class Backup:

    def __init__(self):

        self.sSnapshotPrefix = 'rhbautosnp_'
        self.sLogString = ''

        self.assignDefaultTimingsToAccounts()
        self.run()

    def run(self):
        # Get available regions
        regions = ec2.regions()

        # Get AWS info
        for site,opts in accounts.aws.iteritems(): # Loop accounts
            self.log('[Running for ' + site + ']', 2)
            tmp = regions
            for r in tmp: # Loop regions, per account
                if hasattr(r, 'name'):
                    self.log('[Connecting to region ' + r.name + ']', 3)
                    # Connect to AWS
                    conn = ec2.connection.EC2Connection(
                        opts['key'],
                        opts['secret'],
                        region=r
                    )
                    if conn:
                        # Get volumes for this accounts region
                        vols = conn.get_all_volumes()
                        if vols:
                            self.log('[Fetching snapshots]', 4)
                            # Get all available snapshots
                            snapshots = conn.get_all_snapshots(None, 'self')
                            # Loop volumes
                            for vol in vols:
                                mostRecentSnapshots = {}
                                # Check existing snapshots
                                for snp in snapshots:
                                    if (snp.volume_id == vol.id) and self.isOneOfOurs(snp):
                                        stype = self.getBackupTypeFromDesc(snp)
                                        # Snapshot has expired - delete
                                        if self.doIneedToDeleteThisSnapshot(snp, opts['backup_timings']):
                                            self.log('[Deleting snapshot ' + snp.id + ']', 5)
                                            conn.delete_snapshot(snp.id)
                                        else:
                                            self.log('[Did not need to delete snapshot for ' + snp.id + ']', 5)

                                        # Keep a note of the most up to date snapshot (check if we need to make a new one)
                                        dt = datetime.datetime.strptime(snp.start_time.replace('.000Z', ''), "%Y-%m-%dT%H:%M:%S")
                                        if (stype not in mostRecentSnapshots) or (dt > mostRecentSnapshots[stype]):
                                            mostRecentSnapshots[stype] = dt

                                # Loop through backup types
                                for t,v in opts['backup_timings'].iteritems():
                                    if int(v['interval']) > 0:
                                        bMakeSnapshot = True
                                        if t in mostRecentSnapshots:
                                            # Snapshots already exist for this volume - check to see if a new snapshot is required
                                            if int(v['interval']) is not 1:
                                                if ((mostRecentSnapshots[t] + datetime.timedelta(hours=int(v['interval']))) > datetime.datetime.now()):
                                                    bMakeSnapshot = False

                                        if bMakeSnapshot is True:
                                            snapshot_name = self.generateSnapshotName(vol,t)
                                            conn.create_snapshot(vol.id, snapshot_name)
                                            self.log('[Creating snapshot ' + snapshot_name + ']', 4)

    def isOneOfOurs(self, snp):
        return ('-[' in snp.description and self.sSnapshotPrefix in snp.description)

    def getBackupTypeFromDesc(self, snp):
        tmp = snp.description.split('-[')
        sBackupType = tmp[1].rstrip(']')
        return sBackupType

    def generateSnapshotName(self, vol, stype):
        sname = vol.id
        sname += '_' + self.sSnapshotPrefix
        sname += '~' + datetime.datetime.now().strftime('%d-%m-%Y_%I:%M%p')
        sname += '-[' + stype + ']'
        return sname

    def doIneedToDeleteThisSnapshot(self, snp, timings):
        sBackupType = self.getBackupTypeFromDesc(snp)
        eDt = datetime.datetime.strptime(snp.start_time.rstrip('.000Z'), "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(0, 0, 0, 0, 0, timings[sBackupType]['expire_after'])
        return eDt <= datetime.datetime.now()

    def assignDefaultTimingsToAccounts(self):
        for i,aopts in accounts.aws.iteritems():
            if 'backup_timings' not in aopts:
                accounts.aws[i]['backup_timings'] = {}
            for k,topts in config.backup_timings.iteritems():
                if k not in accounts.aws[i]['backup_timings']:
                    accounts.aws[i]['backup_timings'][k] = {}
                for ki,kv in topts.iteritems():
                    if ki not in accounts.aws[i]['backup_timings'][k]:
                        accounts.aws[i]['backup_timings'][k][ki] = kv

    def log(self, sMsg, iLevel = 0):
        if (iLevel < config.iStopLogsAtLevel) and (iLevel > 0):
            r = range(0,iLevel)
            for i in r:
                sMsg = '~' + sMsg
        if config.bPrintLogMsgs and (config.iStopLogsAtLevel > 0):
            print sMsg
        self.sLogString += sMsg + "\n"

    def __del__(self):
        # Update log file
        if config.bPrintToLogFile:
            f = open(config.sLogFilename, 'a')
            f.write("//-------------[ " + str(datetime.datetime.now()) + " ]-------------//\n" + self.sLogString)
            f.close()

BK = Backup()

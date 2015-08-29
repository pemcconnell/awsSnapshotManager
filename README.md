# snapshot manager

Super simple app that is designed to create snapshots of all ec2 instances it finds across multiple accounts and regions.

## configuration

Ensure that you have created an IAM user with sufficient priviledges to view all EC2 instances & create snapshots for each of the accounts you wish to run this snapshot manager on.

Edit `accounts.py` and add each account. There is a commented example of this in that file. `key` and `secret` are the only required fields. You can also specify the timings if you want more granular control for a specific account.

### run

simply run `backup.py`

### requirements

- python 2.7
- [boto](https://github.com/boto/boto)

### notes

 - default configuration options are set in `config.py`
 - account info and account-specific configs are set in `accounts.py`
 - `backup.py` is the script which handles generating the snapshots

import paramiko #pip3 install paramiko
import os
import datetime
import calendar

path = "/opt/cloudera/parcels/CDH/lib/hadoop/lib"
incident_date = datetime.date(2018, 6, 1)
username = "<>"
password = "<>"
known_hosts = "~/.ssh/known_hosts"
cluster_ips_filename = "cluster_ip.txt"


def process_server(hostname):
    print("Processing " + hostname)
    try:
        ssh.connect(hostname, username=username, password=password)
        sftp = ssh.open_sftp()
        try:
            files = sftp.listdir(path)
            for file in files:
                full_path = os.path.join(path, file)
                stats = sftp.stat(full_path)
                if stats.st_mtime > incident_timestamp:
                    print("File to remove: " + str(full_path)) #uncomment for dry-run
                    #sftp.remove(full_path)
        finally:
            sftp.close()
    finally:
        ssh.close()


incident_timestamp = calendar.timegm(incident_date.timetuple())

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(known_hosts))

with open(cluster_ips_filename, 'r') as cluster_ips_file:
    ips = cluster_ips_file.read().split('\n')
    for ip in ips:
        process_server(ip)

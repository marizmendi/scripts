import boto3
import os
import yaml
import sys
import time
import csv

def load_config():
    with open("config.yml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config

def get_all_open_sgs_ids(ec2):
    result = []
    res = ec2.describe_security_groups()
    sgs = res['SecurityGroups']
    for sg in sgs:
        for rule in sg['IpPermissions']:
            for ip_range in rule['IpRanges']:
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    result.append(sg.get('GroupId'))

    return result

def get_all_attached_sgs_ids(ec2):
    result = []
    res = ec2.describe_network_interfaces()
    enis = res['NetworkInterfaces']
    for eni in enis:
        _sgs = eni.get('Groups')
        for sg in _sgs:
            result.append(sg.get('GroupId'))
    return result

def get_open_sgs(ec2, attached):
    open_sgs = set(get_all_open_sgs_ids(ec2))
    attached_sgs = set(get_all_attached_sgs_ids(ec2))

    if attached:
        return list(open_sgs.intersection(attached_sgs))
    else:
        return list(open_sgs.difference(attached_sgs))

def audit(ec2):
    return get_open_sgs(ec2, attached=True)

def main():
    config = load_config()
    regions = config.get('regions')

    session = boto3.session.Session()

    f = open(account + ".txt","w")
    for region in regions:
        ec2 = session.client('ec2', region_name=region)
        sgs = audit(ec2)
        for sg in sgs:
            output = region + "," + sg
            f.write(output + '\n')
    f.close()

if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

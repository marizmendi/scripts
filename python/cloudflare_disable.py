#!/usr/bin/env python
"""Cloudflare API code - example"""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

EMAIL = #email
TOKEN = #token
CERTTOKEN = #certtoken

def main():
    """Cloudflare API code - example"""

    # Grab the first argument, if there is one
    try:
        zone_name = sys.argv[1]
        params = {'name':zone_name, 'per_page':1}
    except IndexError:
        params = {'per_page':50}

    cf = CloudFlare.CloudFlare(email=EMAIL, token=TOKEN, certtoken=CERTTOKEN)

    # grab the zone identifier
    try:
        zones = cf.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones - %s - api call failed' % (e))

    # there should only be one zone
    for zone in sorted(zones, key=lambda v: v['name']):
        zone_name = zone['name']
        zone_id = zone['id']
        next = True
        while (next):
            try:
                certificates = cf.certificates.get(params={'zone_id':zone_id, 'per_page':10})
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                exit('/zones.ssl.certificate_packs %d %s - api call failed' % (e, e))

            for certificate in certificates:
                cf.certificates.delete(certificate['id'])

            next = len(cf.certificates.get(params={'zone_id':zone_id, 'per_page':10})) > 0

            print(next)

    exit(0)

if __name__ == '__main__':
    main()

import os

def get_sub(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

import argparse
parser = argparse.ArgumentParser(description='obs-studio release util')
parser.add_argument('-d', '--directory', dest='dir', default='.')
parser.add_argument('-u', '--base-url', dest='base_url', default='https://builds.catchexception.org/obs-studio')
args = parser.parse_args()

r = {}
import fnmatch

from xml.etree import ElementTree as ET

ET.register_namespace('sparkle', 'http://www.andymatuschak.org/xml-namespaces/sparkle')
ET.register_namespace('ce', 'http://catchexception.org/xml-namespaces/ce')

def qn_tag(n, t):
    return {
        'ce': str(ET.QName('http://catchexception.org/xml-namespaces/ce', t)),
        'sparkle': str(ET.QName('http://www.andymatuschak.org/xml-namespaces/sparkle', t))
    }[n]

def get_last_item(f):
    t = ET.ElementTree()
    t.parse(f)
    # assume there is a valid version if updates.xml exists
    return t.findall('channel/item')[-1]

for d in get_sub('.'):
    for root, dirs, files in os.walk(d):
      for f in fnmatch.filter(files, 'updates.xml'):
            c = os.path.dirname(os.path.join(root, f))
            i = get_last_item(os.path.join(root, f))
            r[c] = {
                'url': '{0}/{1}/updates.xml'.format(args.base_url, c),
                'date': i.find('pubDate').text,
                'version': i.find('enclosure').get(qn_tag('sparkle', 'shortVersionString'))
            }

import json
with open(os.path.join(args.dir, 'feeds.json'), 'w') as f:
    json.dump(r, f, sort_keys=True, indent=4, separators=(',', ': '))

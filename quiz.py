#!/usr/bin/python3
import argparse
import logging

import dikta

log_levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

ap = argparse.ArgumentParser(description =
    'Interactive Do I Know It Already quiz')
ap.add_argument('json_file', type = argparse.FileType('r'),
    help = 'Quiz in JSON format')
ap.add_argument('--loglevel', dest = 'log_level', default = 'INFO', type = str,
    choices = log_levels.keys(), help = 'Logging verbosity')

args = ap.parse_args()

logging.basicConfig(level = args.log_level)

logging.debug('Loading from "%s"' % args.json_file.name)

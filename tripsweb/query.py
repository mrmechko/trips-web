#!/usr/bin/env python

import sys
import urllib.parse as uparse
import urllib.request as urequest
import argparse
import json
from . import process


# 1.
TRIPS_URL="http://trips.ihmc.us/parser/cgi/step"

def arguments():
    parser = argparse.ArgumentParser(description='Query the trips webparser')

    parser.add_argument('input', type=str, nargs=1, help='the text to be parsed', default="")

    parser.add_argument('-s', '--skeleton-score', default=False, help='use skeleton score module', action='store_true')
    parser.add_argument('--tag-type', type=str, metavar='P', nargs='+', help='tag-type hints for the parser.  See online documents for further information')
    parser.add_argument('-u', '--parser-url', type=str, metavar='P', nargs=1, help='the URL of the parser to be used.', default=TRIPS_URL)

    parser.add_argument('-t', '--input-terms', metavar='T', type=str, nargs='+', help='fix tags for specific words in the input.')

    parser.add_argument('-n', '--no-sense', metavar='W', type=str, nargs=1, help="comma separated list of words that text-tagger will delegate to the trips lexicon for sense information")
    parser.add_argument('-p', '--penn-senses', metavar='POS', type=str, nargs=1, help="comma separated list of Penn tags that TextTagger output sense info for (default is all)")
    parser.add_argument('--component', type=str, nargs=1, help="run the parser or texttagger only", metavar="parser|texttagger")
    parser.add_argument('-c', '--config', type=str, nargs=1, help='a json config file describing the parse')
    parser.add_argument('-d', '--dump', default=False, action="store_true", help="print a config file instead")
    parser.add_argument('-x', '--xml', default=False, action="store_true", help="dump the parse as xml instead of json")


    return parser


def main():
    args = arguments().parse_args()

    url = args.parser_url
    parameters = {}
    if args.config:
        # load from config if it exists
        parameters = config.load(open(args.config))
    if not args.dump and args.input == "" and 'input' not in parameters:
        print("error: please specify input either via cmdline or config file", file=sys.stderr)
        return -1
    else:
        parameters['input'] = args.input
    if args.tag_type:
        parameters['tag-type'] = args.tag_type
    if args.input_terms:
        parameters['input-terms'] = args.input_terms
    if args.no_sense:
        parameters['no-sense-words'] = args.no_sense
    if args.penn_senses:
        parameters['senses-only-for-penn-poss'] = args.penn_senses
    if args.skeleton_score:
        parameters['semantic-skeleton-scoring'] = True

    if args.dump:
        print(json.dumps(parameters))
        return 0

    data = uparse.urlencode(parameters)
    data = data.encode('ascii')
    with urequest.urlopen(url, data) as response:
        result = response.read().decode("utf-8")
        if args.xml:
            print(result)
            return 0
        else:
            print(process.read(result))
            return 0


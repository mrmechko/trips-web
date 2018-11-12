#!/usr/bin/env python

import sys
import urllib.parse as uparse
import urllib.request as urequest
import argparse
import json
from tripsweb import process


# 1.
TRIPS_URL="http://trips.ihmc.us/parser/cgi/step"

def arguments():
    parser = argparse.ArgumentParser(description='Query the trips webparser')

    parser.add_argument('input', type=str, nargs=1, help='the text to be parsed', default="")


    parser.add_argument('-s', '--skeleton-score', default=False, help='use skeleton score module', action='store_true')
    parser.add_argument('--tag-type', type=str, metavar='P', nargs='+', help='tag-type hints for the parser.  See online documents for further information')
    parser.add_argument('-u', '--parser-url', type=str, metavar='P', nargs=1, help='the URL of the parser to be used.', default=TRIPS_URL)

    parser.add_argument('-t', '--input-terms', metavar='T', type=str, nargs='1', help='file containing input-terms.  See make-input-terms --help for more details.')

    parser.add_argument('-n', '--no-sense', metavar='W', type=str, nargs=1, help="comma separated list of words that text-tagger will delegate to the trips lexicon for sense information")
    parser.add_argument('-p', '--penn-senses', metavar='POS', type=str, nargs=1, help="comma separated list of Penn tags that TextTagger output sense info for (default is all)")
    parser.add_argument('--component', type=str, nargs=1, help="run the parser or texttagger only", metavar="parser|texttagger")

    # these params don't go to the json.
    parser.add_argument('-c', '--config', type=str, nargs=1, help='a json config file describing the parse')
    parser.add_argument('-d', '--dump', default=False, action="store_true", help="print a config file instead")
    parser.add_argument('-x', '--xml', default=False, action="store_true", help="dump the parse as xml instead of json")
    parser.add_argument('-v', '--verbose', default=False, help="print debug output to stderr", action='store_true')


    return parser


def get_input_terms(fname):
    iterms = json.load(open(fname))
    if type(iterms) is dict:
        iterms = [iterms]
    def proc_entry(entry, is_list=False):
        if is_list and not type(entry) is list:
            entry = [entry]
        if type(entry) is not list:
            return str(entry)
        return "({})".format(" ".join([str(e) for e in entry]))

    def process(term):
        """
        :lex str
        :wn-sense-keys list
        :penn-pos list
        :lftypes list
        :penn-cat list(?)
        """
        key, val = term
        as_list = key in ["wn_sense_keys", "penn_pos", "lftypes", "penn_cat"]
        return " ".join(":"+key.replace("_", "-"), proc_entry(val, as_list)]

    res = ["(sense {})".format(" ".join([process(t) for t in term.items()])) for term in iterms]
    return "({})".join(res)



def main():
    args = arguments().parse_args()

    url = args.parser_url
    parameters = {}
    tag_type = set()
    if args.config:
        # load from config if it exists
        parameters = json.load(open(args.config))
    if not args.dump and args.input == "" and 'input' not in parameters:
        print("error: please specify input either via cmdline or config file", file=sys.stderr)
        return -1
    else: 
        parameters['input'] = args.input
    if args.tag_type:
        tag_type.update(args.tag_type)
    if args.input_terms:
        parameters['input-terms'] = get_input_terms(args.input_terms)
        tag_type.add("terms-input")
    if args.no_sense:
        parameters['no-sense-words'] = args.no_sense
    if args.penn_senses:
        parameters['senses-only-for-penn-poss'] = args.penn_senses
    if args.skeleton_score:
        parameters['semantic-skeleton-scoring'] = True

    if tag_type:
        tag_type.add("default")
        parameters['tag-type'] = "(or" + " ".join(tag_type) + ")"

    if args.dump:
        print(json.dumps(parameters))
        return 0

    verbose = args.verbose
    as_xml = args.xml
    result, code = get_parse(url, parameters, as_xml, verbose)
    print(result)
    return code

def get_parse(url, parameters, as_xml, verbose, return_response=False):
    if verbose:
        print("parameters:\n", parameters, file=sys.stderr)
    data = uparse.urlencode(parameters)
    if verbose:
        print("data:\n", data, file=sys.stderr)

    data = data.encode('ascii')

    with urequest.urlopen(url, data) as response:
        if return_response:
            return response
        result = response.read()
        if verbose:
            print("Result:\n", result, file=sys.stderr)
        result = result.decode("utf-8")
        if verbose:
            print("decoded:\n", result, file=sys.stderr)
        if as_xml:
            return result, 0
        else:
            return process.read(result), 0


import sys
import json
import argparse

def arguments():
    """
    :lex str
    :wn-sense-keys list
    :penn-pos list
    :lftypes list
    :penn-cat list(?)
    """

    parser = argparse.ArgumentParser(description="build input_terms entry for a trips parser request")
    "lex"
    parser.add_argument('-f', '--file', type=str, metavar="F", nargs=1, help="File to write the term to")
    parser.add_argument('-l', '--lex', type=str, metavar='L', nargs=1, help='the word you want to hint')
    parser.add_argument('-w', '--wn-sense-keys', type=str, metavar="W", nargs='+', help="WordNet senses associated", default=[])
    parser.add_argument('-p', '--penn-pos', type=str, metavar="P", nargs='+', help="parts of speech (Penn tags)", default=[])
    parser.add_argument("-o", '--lftypes', type=str, metavar="ont::T", nargs='+', help="ontology types (prefixed with 'ont::'", default=[])
    parser.add_argument("-c", '--penn-cat', type=str, metavar="C", nargs='+', help="penn cats", default=[])


def make_input_terms(lex, wn_sense_keys=[], penn_pos=[], lftypes=[], penn_cat=[], insert=None):
    res = {
            "lex": lex,
            "wn_sense_keys": wn_sense_keys,
            "penn_pos": penn_pos,
            "lftypes": ["ont::"+x.split("ont::")[-1] for x in lftypes],
            "penn_cat": penn_cat
        }
    if not insert:
        return res
    if "input_terms" not in insert:
        insert['input_terms'] = [res]
    else:
        insert['input_terms'].append(res)


def main():
    args = arguments().parse_args()
    insert = None
    if args.file:
        insert = json.read(open(args.file))
    result = make_input_terms(args.lex, args.wn_sense_keys, args.penn_pos, args.lftypes, args.penn_cat, insert)
    if args.outfile:
        with open(args.outfile, 'w') as out:
            json.dump(result, out)
    else:
        print(result)
    return 0

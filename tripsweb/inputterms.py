import sys
import json
import argparse
import os

def arguments():
    """
    :lex str
    :wn-sense-keys list
    :penn-pos list
    :lftype list
    :penn-cat list(?)
    """

    parser = argparse.ArgumentParser(description="build input_terms entry for a trips parser request")
    parser.add_argument("--force", default=False, help="Force writing to output file even if it already exists", action="store_true")
    parser.add_argument('-f', '--file', type=str, metavar="F", help="file to read the containing config from", default="")
    parser.add_argument('-x', '--outfile', type=str, metavar="F", help="File to write the term to", default=[])
    parser.add_argument('-u', '--update', type=str, metavar="F", help="update a config file with an input term", default=[])
    parser.add_argument('-l', '--lex', type=str, metavar='L', help='the word you want to hint')
    parser.add_argument('-w', '--wn-sense-keys', type=str, metavar="W", nargs='+', help="WordNet senses associated", default=[])
    parser.add_argument('-p', '--penn-pos', type=str, metavar="P", nargs='+', help="parts of speech (Penn tags)", default=[])
    parser.add_argument("-o", '--lftype', type=str, metavar="ont::T", nargs='+', help="ontology types (prefixed with 'ont::')", default=[])
    parser.add_argument("-c", '--penn-cat', type=str, metavar="C", nargs='+', help="penn cats", default=[])
    parser.add_argument("-s", '--score', type=float, metavar="S", help="score for entry", default=-1)
    parser.add_argument("-t", '--start', type=int, metavar="S", help="span start", default=-1)
    parser.add_argument("-e", '--end', type=int, metavar="S", help="span end", default=-1)
    return parser

def _check_percent(w):
    if "%" in w and "\\%" not in w:
        w = w.replace("%", "\\%")
    return w

def make_input_terms(lex, wn_sense_keys=[], penn_pos=[], lftype=[], penn_cat=[], score=-1, start=-1, end=-1, insert=None):
    res = []
    if lex:
        res.append(":lex \"%s\"" % lex)
    if wn_sense_keys:
        res.append(":wn-sense-keys (%s)" % " ".join(['"%s"' % s for s in wn_sense_keys]))
    if penn_pos:
        res.append(":penn-parts-of-speech (%s)" % " ".join(penn_pos))
    if penn_cat:
        res.append(":penn-cat (%s)" % " ".join(penn_cat))
    if lftype:
        res.append(":lftype (%s)" % " ".join(lftype))
    if score >= 0:
        res.append(":score " + str(score))
    res.append(":start " + str(start))
    res.append(":end " + str(end))

    if lftype:
        res = "(sense %s)" % " ".join(res)
    else:
        res = "(pos %s)" % " ".join(res)

    if not insert:
        return [res]
    if type(insert) is list:
        insert.append(res)
    elif type(insert) is dict:
        if "input-tags" not in insert:
            insert['input-tags'] = [res]
        else:
            insert['input-tags'].append(res)
    return insert


def main():
    args = arguments().parse_args()
    if not args.lex:
        print("error: please specify a lex item to attach the term to", file=sys.stderr)
        return -1
    insert = None
    infile, outfile = None, None
    if args.file:
        infile = args.file
        print("reading from {}".format(infile), file=sys.stderr)
    if args.outfile:
        outfile = args.outfile
        print("writing to {}".format(outfile), file=sys.stderr)        
    if args.update:
        infile, outfile = args.update, args.update
        print("updating {}".format(infile), file=sys.stderr)

    force = args.force or args.update

    if infile:
        insert = json.load(open(infile))

    result = make_input_terms(args.lex, args.wn_sense_keys, args.penn_pos, args.lftype, args.penn_cat, args.score, args.start, args.end, insert)

    if outfile:
        if os.path.isfile(outfile) and not force:
            print("Warning: Output file exists.  Specify --force to write")
        with open(outfile, 'w') as out:
            json.dump(result, out)
    else:
        print(result)
    return 0

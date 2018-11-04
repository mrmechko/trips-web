import pprint, json, xmltodict
from collections import namedtuple, OrderedDict

js = xmltodict.parse(open("test.xml").read())
terms = js['trips-parser-output']["utt"]["terms"]["rdf:RDF"]["rdf:Description"]

# @rdf:ID, LF:indicator, LF:type, role:*, LF:start, LF:end

def find_terms(stream):
    js = xmltodict.parse(stream)['trips-parser-output']
    if 'compound-communication-act' in js:
        return js['compound-communication-act']['utt']
    else:
        return [js['utt']]


INode = namedtuple("INode", ['id', 'indicator', 'type', 'word', 'roles', 'start', 'end'])
IRole = namedtuple("IRole", ["role", "target"])


def val_or_ref(y):
    if type(y) is OrderedDict:
        return y.get("@rdf:resource", None)
    return y

def get_roles(term):
    return [IRole(x.split(":")[-1], val_or_ref(y)) for x, y in term.items() if x.startswith("role:")]

def as_json(utt):
    try:
        terms = utt["terms"]["rdf:RDF"]["rdf:Description"]
        return {n["@rdf:ID"]: INode(
            n.get("@rdf:ID", None),
            n.get("LF:indicator", None),
            n.get("LF:type", None),
            n.get("LF:word", None),
            get_roles(n),
            int(n.get("LF:start", -1)),
            int(n.get("LF:end", -1))) for n in terms}
    except Error:
        return {}

def read(stream):
    terms = find_terms(stream)
    return [as_json(t) for t in terms]

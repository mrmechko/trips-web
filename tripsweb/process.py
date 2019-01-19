import json, xmltodict
from collections import namedtuple, OrderedDict

# @rdf:ID, LF:indicator, LF:type, role:*, LF:start, LF:end

def find_terms(stream):
    js = xmltodict.parse(stream)['trips-parser-output']
    if 'compound-communication-act' in js:
        return js['compound-communication-act']['utt']
    else:
        return [js['utt']]


def val_or_ref(y):
    if type(y) is OrderedDict:
        return y.get("@rdf:resource", None)
    return y

def get_roles(term):
    return {x.split(":")[-1] : val_or_ref(y) for x, y in term.items() if x.startswith("role:")}

def as_json(utt):
    if type(utt) is list:
        return [as_json(u) for u in utt]
    terms = utt["terms"]["rdf:RDF"]["rdf:Description"]
    root = terms[0]["@rdf:ID"]
    result = {n["@rdf:ID"]: {
        "id": n.get("@rdf:ID", None),
        "indicator":n.get("LF:indicator", None),
        "type": n.get("LF:type", None),
        "word": n.get("LF:word", None),
        "roles":get_roles(n),
        "start": int(n.get("LF:start", -1)),
        "end": int(n.get("LF:end", -1))
        } for n in terms}
    result["root"] = root
    return result

def read(stream):
    terms = find_terms(stream)
    return json.dumps([as_json(t) for t in terms], indent=2)

import json, xmltodict
from collections import namedtuple, OrderedDict

# @rdf:ID, LF:indicator, LF:type, role:*, LF:start, LF:end

def find_utts(dct):
    utts = []
    for k, v in dct.items():
        if k.lower() == "utt":
            utts += [v]
        elif isinstance(v, dict):
            utts += find_utts(v)
        elif type(v) is list:
            utts += [find_utts(x) for x in v]
    return utts

def find_terms(stream):
    js = xmltodict.parse(stream)
    inputtags = js['trips-parser-output'].get("@input-tags", [])
    debug = js['trips-parser-output']["debug"]
    return find_utts(js), inputtags, debug


def val_or_ref(y):
    if type(y) is OrderedDict:
        return y.get("@rdf:resource", None)
    elif type(y) is list:
        return [val_or_ref(x) for x in y]
    return y

def get_roles(term):
    return {x.split(":")[-1] : val_or_ref(y) for x, y in term.items() if x.startswith("role:")}

def as_json(utt):
    if type(utt) is list:
        return [x for x in [as_json(u) for u in utt] if x]
    try:
        terms = utt["terms"]["rdf:RDF"]["rdf:Description"]
        root = utt["terms"]["@root"] #terms[0]["@rdf:ID"]
        if type(terms) is OrderedDict:
            terms = [terms]
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
    except:
        return None

def _flat(x):
    if isinstance(x, list):
        return sum([_flat(y) for y in x], [])
    else:
        return [x]

def read(stream, debug=False):
    terms, inputtags, debug = find_terms(stream)
    res = [as_json(t) for t in terms]
    if debug:
        return json.dumps({"parse": _flat(res), "inputtags": inputtags, "debug": debug.split("\n")}, indent=2)
    return json.dumps(res, indent=2)

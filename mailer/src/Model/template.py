from Controller.basic import check
from Object.template import Template
import json

def template_list(cn, nextc):
    err = Template("").list()
    return cn.call_next(nextc, err)

def template_get(cn, nextc):
    err = check.contain(cn.rt, ["template"], "PATH")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.private['template'] = Template(cn.rt['template'])
    err = cn.private['template'].get()
    return cn.call_next(nextc, err)

def template_new(cn, nextc):
    err = check.contain(cn.pr, ["name", "template"], "BODY")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Template(cn.pr["name"]).new(cn.pr["template"])
    return cn.call_next(nextc, err)

def template_customize(cn, nextc):
    err = check.contain(cn.pr, ["variables"], "BODY")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private['template'].customize(cn.pr["variables"])
    if err[0]:
        cn.private["render"] = err[1]
    return cn.call_next(nextc, err)

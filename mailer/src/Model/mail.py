from Controller.basic import check
from Object.mail import Mail
import json

def mail_list(cn, nextc):
    expand = 'expand' in cn.get
    err = Mail().list(expand)
    return cn.call_next(nextc, err)

def mail_get(cn, nextc):
    err = check.contain(cn.rt, ["mail"], "PATH")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.private['template'] = Mail()
    err = cn.private['template'].get()
    return cn.call_next(nextc, err)

def mail_new(cn, nextc):
    err = check.contain(cn.pr, ["to", "subject"], "BODY")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Mail().new(cn.pr["to"], cn.pr["subject"], cn.private["render"])
    return cn.call_next(nextc, err)

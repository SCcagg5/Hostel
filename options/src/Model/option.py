from Controller.basic import check
from Object.option import Option

def option_get(cn, nextc):
    err = check.contain(cn.pr, ["options"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Option().get(cn.pr['options'])
    return cn.call_next(nextc, err)

def option_book(cn, nextc):
    err = check.contain(cn.pr, ["options"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Option().book(cn.pr['options'])
    return cn.call_next(nextc, err)

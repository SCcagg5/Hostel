from Controller.basic import check
from Object.hotel import Hotel

def hotel_init(cn, nextc):
    id = cn.private["sso"].user["id"] if 'sso' in cn.private else None
    cn.private["hotel"] = Hotel(user_id = id)
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def hotel_get(cn, nextc):
    err = check.contain(cn.get, [["date", 'from']], 'GET')
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = check.contain(cn.rt, ["hotel"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["hotel"].get_by_id(cn.rt["hotel"], cn.get["date"])
    return cn.call_next(nextc, err)

def hotel_book(cn, nextc):
    err = check.contain(cn.get, ["from", "to"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    token = True if "token" in cn.get else False
    err = check.contain(cn.pr, ["book"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["hotel"].book(book=cn.pr["book"], token=token, fromdate=cn.get["from"], todate=cn.get["to"])
    return cn.call_next(nextc, err)

def hotel_update(cn, nextc):
    err = check.contain(cn.pr, ["name", "options"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["hotel"].update(cn.pr["name"], cn.pr["options"])
    return cn.call_next(nextc, err)

def hotel_pay(cn, nextc):
    err = check.contain(cn.pr, ["token"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private["hotel"].pay(cn.pr["token"])
    return cn.call_next(nextc, err)

from Controller.basic import check
from Object.room import Room

def room_get(cn, nextc):
    err = check.contain(cn.pr, ["rooms", "date"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Room().get(cn.pr['rooms'], cn.pr['date'])
    return cn.call_next(nextc, err)

def room_book(cn, nextc):
    err = check.contain(cn.pr, ["rooms", "date"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Room().book(cn.pr['rooms'], cn.pr['date'])
    return cn.call_next(nextc, err)

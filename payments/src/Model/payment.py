from Controller.basic import check
from Object.payment import Payment

def payment_get(cn, nextc):
    err = check.contain(cn.pr, ["book"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Payment.get(cn.pr['book'])
    return cn.call_next(nextc, err)

def payment_pay(cn, nextc):
    err = check.contain(cn.pr, ["token"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Payment.pay(cn.pr['token'])
    return cn.call_next(nextc, err)

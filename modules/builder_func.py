#!/usr/bin/python

from logger import SIXAnalyzer_logger

## @brief del $to_find from existing meth
#  to check the signature with other meths
## @param meth method to find
## @returns meth string without $to_find
def over_meth(meth):
    meth = meth.replace("NS_IMETHOD_ ", "")
    meth = meth.replace("NS_IMETHOD ", "")
    meth = meth.replace("virtual ", "")
    meth = meth.replace("  ", " ")
    return (meth)

def is_macro(bar):
    par = 0
    for i in range(len(bar)):
        if (not bar[i].isupper() and not bar[i] == '_' and not bar[i] == '(' and not bar[i] == ')' and not bar == ":"):
            return False
    return True

def check_ret_namespace(bar):
    res = ""
    start = bar.rfind("::")
    if (start == -1):
        return (bar)
    end = bar.rfind(" ", 0, start)
    if (end == -1):
        res = ""
    res = bar[:end + 1]
    res += bar[start + 2:]
    SIXAnalyzer_logger.print_debug("Ret: " + bar + " => " + res)
    return (res)

def check_ret(bar):
    if (bar.find("NS_IMETHOD") == 0):
        return check_ret_namespace(bar)
    words = bar.split(' ')
    j = 0
    for i in range(len(words)):
        if is_macro(words[i]) == False:
            res = " ".join(words[i:])
            if (res == "*" or res == "&"):
                return check_ret_namespace(bar)
            return check_ret_namespace(res)
        else:
            j = j + 1
    if i == j - 1:
        return ""
    return check_ret_namespace(bar)

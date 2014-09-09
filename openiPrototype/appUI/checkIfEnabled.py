def checkIfEnabled(text):
    if (str(text).lower()=='disabled') or (str(text).lower()=='false') or (text is None):
        return False
    elif (str(text).lower()=='enabled') or (str(text).lower()=='on'):
        return True
    return False



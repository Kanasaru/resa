import data.errorcodes as errorcodes


def set_attr(attr_target, attr_source):
    if isinstance(attr_source, tuple) and len(attr_source) == 2:
        if attr_source[0] in attr_target:
            attr_target[attr_source[0]] = attr_source[1]
        else:
            print(errorcodes.E_KEY)
            return False
    elif isinstance(attr_source, dict):
        for key, value in attr_source.items():
            if key in attr_target:
                attr_target[key] = value
            else:
                print(errorcodes.E_KEY)
    else:
        print(errorcodes.E_FORMAT)
        return False
    return True


def get_attr(attr_target, key=None):
    if key is not None:
        if isinstance(key, str):
            if key in attr_target:
                return attr_target[key]
            else:
                print(errorcodes.E_KEY)
                return False
        else:
            print(errorcodes.E_KEYTYPE)
            return False
    else:
        return attr_target

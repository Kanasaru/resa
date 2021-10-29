import data.helpers.error

resa_error_list = data.helpers.error.ErrorList()

E_KEY = 10001
resa_error_list.add(data.helpers.error.Error(E_KEY, "Given key does not exist"))
E_KEYTYPE = 10002
resa_error_list.add(data.helpers.error.Error(E_KEYTYPE, "Wrong type of given key"))
E_FORMAT = 10003
resa_error_list.add(data.helpers.error.Error(E_FORMAT, "Wrong format of given attributes"))

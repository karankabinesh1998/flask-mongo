from src.constants.route_constants import APP_USER,APP_AUTH_LOGIN
def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def skip_urls():
        return [APP_USER,APP_AUTH_LOGIN]

auth_constants = _Const()
from functools import wraps


def make_secure(func):
    @wraps(func)
    def secure_func():
        if user['access'] == True:
            return func()
        else:
            return 'Permission denied'
    return secure_func


@make_secure
def admin_pass():
    return 'PassWord!'


user = {'name': 'Ali', 'access': True}




print(admin_pass.__name__)
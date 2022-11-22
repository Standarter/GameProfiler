import time
def functime(verbose=True):
    def functime_decor(func):
        def wrapper(*kargs, **kwargs):
            T1 = time.time()
            Result = func(*kargs, **kwargs)
            if verbose:
                print("Function {0} takes {1} seconds".format(func.__name__, time.time() - T1))
            return Result
        return wrapper
    return functime_decor
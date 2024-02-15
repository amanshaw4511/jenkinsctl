

def use_vprint(verbose_flag):
    def vprint(*args, **kwargs):
        if verbose_flag:
            print(*args, **kwargs)

    return vprint

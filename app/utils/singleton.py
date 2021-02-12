class Singleton:
    class _Singleton:
        pass

    _instance = None

    def __init__(self, *args, **kwargs):
        if not Singleton._instance:
            Singleton._instance = Singleton._Singleton(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

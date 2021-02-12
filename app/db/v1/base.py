import abc

from app.utils.singleton import Singleton


class BaseDB(Singleton, metaclass=abc.ABCMeta):
    """The parent class for all the databases that are to come later on.

    Inherit this class for every new concrete class that you wish to implement
    inside the `databases` directory.
    """

    @abc.abstractproperty
    def dbname(self):
        ...

    @abc.abstractmethod
    async def count(self, *args, **kwrags):
        ...

    @abc.abstractmethod
    async def insert_one(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def delete_one(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def update_one(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def read_one(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def read_many(self, *args, **kwargs):
        ...

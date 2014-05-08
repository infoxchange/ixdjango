"""
Database router
"""


class MasterSlaveRouter(object):
    """
    A master/slave router for IXDjango

    Redirects all reads to standby and all writes to default
    """

    MASTER = 'default'
    SLAVE = 'standby'

    def db_for_read(self, model, *hints):
        return self.SLAVE

    def db_for_write(model, *hints):
        return self.MASTER

    def allow_relation(self, obj1, obj2, **hints):
        dbs = set((MASTER, SLAVE))

        if obj1._state.db in dbs and \
           obj2._state.db in dbs:
            return True

        return None

    def allow_syncdb(self, db, model):
        return db == self.MASTER

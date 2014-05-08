"""
Database router
"""


class MasterSlaveRouter(object):
    """
    A master/slave router for IXDjango

    Redirects all reads to standby and all writes to default
    """

    # pylint:disable=unused-argument

    MASTER = 'default'
    SLAVE = 'standby'

    def db_for_read(self, model, *hints):
        """
        Return the DB to use for reads
        """

        return self.SLAVE

    def db_for_write(self, model, *hints):
        """
        Return the DB to use for writes
        """

        return self.MASTER

    def allow_relation(self, obj1, obj2, **hints):
        """
        Determine whether relationships are allowed between the databases
        (i.e. are they clones who share the same foreign keys)
        """

        dbs = set((self.MASTER, self.SLAVE))

        # pylint:disable=protected-access
        if obj1._state.db in dbs and \
           obj2._state.db in dbs:
            return True

        return None

    def allow_syncdb(self, db, model):  # pylint:disable=invalid-name
        """
        Return true if the DB can have it's schema synced
        """

        return db == self.MASTER

import logging

logger = logging.getLogger(__name__)


class Result:

    def __init__(self):
        self._data = {}
        self._bandwidth = 0
        self._max_user = 0

    def add(self, date, hour, server, bandwidth, max_user):
        key = (date, hour, server)
        value = (bandwidth, max_user)
        self._data[key] = value

    def set_default(self, bandwidth, max_user):
        self._bandwidth = bandwidth
        self._max_user = max_user

    def get(self, date, hour, server):
        key = (date, hour, server)
        try:
            return self._data[key]
        except KeyError:
            logger.info('Used default values for {}'.format(key))
            return self._bandwidth, self._max_user

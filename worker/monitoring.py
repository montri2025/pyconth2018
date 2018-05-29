from statsd import StatsClient
from config import STATSD_HOST, STATSD_PORT, STATSD_PREFIX
import logging


try:
    statsd = StatsClient(STATSD_HOST, STATSD_PORT, STATSD_PREFIX, 512)
    print('starting with config host:{} port:{} prefix:{}'.format(STATSD_HOST, STATSD_PORT, STATSD_PREFIX))
except Exception:
    print('can not start statsd with config host:{} port:{} prefix:{}'.format(STATSD_HOST, STATSD_PORT, STATSD_PREFIX))
    statsd = StatsClient()
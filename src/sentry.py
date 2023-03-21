import sys
import os


def init():
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/pkg")
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://eb1e0a669c5e407094c41a6197e03d1e@o4504598752526336.ingest.sentry.io/4504598757834753",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

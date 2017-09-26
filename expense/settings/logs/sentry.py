import os
import raven
from ..base import config

RAVEN_CONFIG = {
    'dsn': config.get("sentry", "dns"),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

import os
import logging
log = logging.getLogger('atlastools')
if not os.environ.get("DEBUG", False):
    log.setLevel(logging.INFO)
if hasattr(logging, 'captureWarnings'):
    logging.captureWarnings(True)

__all__ = ['log']

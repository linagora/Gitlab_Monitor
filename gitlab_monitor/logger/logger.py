# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

""" Logger configuration module. For now, it acts like a classic print.
"""

import logging


def set_verbose(verbose) -> None:
    """Set the verbose mode.

    :type value: bool
    """
    if verbose:
        # DEBUG MODE
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s: %(message)s",
        )
    else:
        # BASIC MODE
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
        )


logger = logging.getLogger("simple_logger")

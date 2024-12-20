# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

""" Logger configuration module. For now, it acts like a classic print.
"""

import logging


# # BASIC MODE
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(message)s",
# )

# DEBUG MODE: à utiliser si avec un --verbose ?
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger("simple_logger")

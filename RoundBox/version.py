#  -*- coding: utf-8 -*-

from typing import Final

MAJOR_VERSION: Final = 1
MINOR_VERSION: Final = 0
PATCH_VERSION: Final = ''
__short_version__: Final = f"{MAJOR_VERSION}.{MINOR_VERSION}"

if PATCH_VERSION:
    __version__: Final = f"{__short_version__}.{PATCH_VERSION}"
else:
    __version__: Final = f"{__short_version__}"

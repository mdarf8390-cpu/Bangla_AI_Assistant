"""
================================================================
AYESHA AI - CACHE SYSTEM
Version : 1.0.0

Purpose:
Fast temporary data storage layer.

Features:
- Key value storage
- Expiration support
- Logging
- Type hints
- Error handling
- Future database integration
================================================================
"""

import logging
import time
from typing import Any, Dict, Optional


logger = logging.getLogger("AYESHA_CORE")



class CacheItem:

    def __init__(
        self,
        value: Any,
        expire: Optional[int] = None
    ):

        self.value = value

        self.created = time.time()

        self.expire = expire



    def expired(self) -> bool:

        if self.expire is None:

            return False


        return (
            time.time() - self.created
            >= self.expire
        )




class CacheManager:


    def __init__(self):

        self.storage: Dict[str, CacheItem] = {}

        logger.info(
            "Cache System Initialized"
        )



    # ----------------------------------------------------------
    # Set Cache
    # ----------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ):

        self.storage[key] = CacheItem(
            value,
            expire
        )


        logger.info(
            f"Cache Stored: {key}"
        )



    # ----------------------------------------------------------
    # Get Cache
    # ----------------------------------------------------------

    def get(
        self,
        key: str
    ) -> Optional[Any]:


        if key not in self.storage:

            return None



        item = self.storage[key]


        if item.expired():

            self.delete(key)

            logger.info(
                f"Cache Expired: {key}"
            )

            return None



        return item.value



    # ----------------------------------------------------------
    # Check Exists
    # ----------------------------------------------------------

    def exists(
        self,
        key: str
    ) -> bool:

        return self.get(key) is not None



    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete(
        self,
        key: str
    ):

        if key in self.storage:

            del self.storage[key]


            logger.info(
                f"Cache Deleted: {key}"
            )



    # ----------------------------------------------------------
    # Clear
    # ----------------------------------------------------------

    def clear(self):

        self.storage.clear()


        logger.info(
            "Cache Cleared"
        )



# Global Cache

cache = CacheManager()
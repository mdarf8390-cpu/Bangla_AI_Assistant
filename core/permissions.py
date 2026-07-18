"""
================================================================
AYESHA AI - PERMISSION SYSTEM
Version : 1.0.0

Purpose:
Controls access before executing actions.

Features:
- Permission rules
- Role based access
- Logging
- Type hints
- Error handling
- Future security integration
================================================================
"""

import logging
from typing import Dict, List


logger = logging.getLogger("AYESHA_CORE")


# ===============================================================
# Permission Manager
# ===============================================================

class PermissionManager:


    def __init__(self):

        # Default permissions

        self.permissions: Dict[str, bool] = {

            "system.open_app": True,

            "browser.open": True,

            "file.read": True,

            "file.write": True,

            "file.delete": False,

            "system.shutdown": False

        }


        logger.info(
            "Permission System Initialized"
        )



    # -----------------------------------------------------------
    # Check Permission
    # -----------------------------------------------------------

    def check(
        self,
        action: str
    ) -> bool:


        try:

            if action in self.permissions:

                result = self.permissions[action]


                logger.info(
                    f"Permission Check: {action} = {result}"
                )


                return result



            logger.warning(
                f"Unknown Permission: {action}"
            )


            return False



        except Exception as error:


            logger.error(
                f"Permission Error: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Grant Permission
    # -----------------------------------------------------------

    def grant(
        self,
        action: str
    ):


        self.permissions[action] = True


        logger.info(
            f"Permission Granted: {action}"
        )



    # -----------------------------------------------------------
    # Revoke Permission
    # -----------------------------------------------------------

    def revoke(
        self,
        action: str
    ):


        self.permissions[action] = False


        logger.info(
            f"Permission Revoked: {action}"
        )



    # -----------------------------------------------------------
    # List Permissions
    # -----------------------------------------------------------

    def all_permissions(
        self
    ) -> Dict[str, bool]:

        return self.permissions.copy()



    # -----------------------------------------------------------
    # Add New Permission
    # -----------------------------------------------------------

    def add_permission(
        self,
        action: str,
        allowed: bool = False
    ):


        self.permissions[action] = allowed


        logger.info(
            f"New Permission Added: {action}"
        )



# ===============================================================
# Global Instance
# ===============================================================

permissions = PermissionManager()
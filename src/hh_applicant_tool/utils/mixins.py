from __future__ import annotations

from functools import cache
from importlib.metadata import version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main import HHApplicantTool


@cache
def get_package_version() -> str | None:
    return version("hh-applicant-tool")


class MegaTool:
    def _check_system(self: HHApplicantTool):
        pass

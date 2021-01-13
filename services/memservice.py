from dataclasses import dataclass
from typing import Optional

from models.runmem import RuntimeMemory

__locator: Optional['MemoryService'] = None


@dataclass
class MemoryService:
    _mem: RuntimeMemory

    @staticmethod
    def init(mem: RuntimeMemory):
        global __locator
        __locator = MemoryService(mem)

    @staticmethod
    def fetch_memory() -> RuntimeMemory:
        global __locator
        if __locator is None:
            raise AttributeError("Service not initialized")

        return __locator._mem

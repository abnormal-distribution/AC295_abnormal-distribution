from abc import ABC, abstractmethod
from typing import List


class Extractor(ABC):

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    @property
    @abstractmethod
    def name(self):
        """Name of the extractor"""

        raise NotImplementedError

    @abstractmethod
    def extract(self, raw_submission: str) -> List[str]:
        """
        Extract contracts documents from a raw eXtensible Business Reporting Language submission
        :param raw_submission: raw XBRL submission
        :return: list of extracted contracts
        """

        raise NotImplementedError

from enum import StrEnum

from pydantic import BaseModel


class FileType(StrEnum):
    PDF = 'pdf'
    CSV = 'csv'


class FileInfo(BaseModel):
    name: str
    type: FileType
    year: str | None = None


class BankInfo(BaseModel):
    name: str
    files: list[FileInfo]

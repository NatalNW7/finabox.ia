from pandas import DataFrame, read_csv
import tabula
from PyPDF2 import PdfReader


from os.path import join


class Pdf(PdfReader):
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
        self.file_path = file_path

    @property
    def total_pages(self) -> int:
        return len(self.pages)

    def to_dataframe(self, pages, header=None) -> DataFrame:
        dfs = tabula.io.read_pdf(self.file_path, pages=pages)

        if len(dfs) > 1:
            output_file = join(BASE, "output.csv")
            tabula.convert_into(self.file_path, output_file, output_format="csv", pages=pages)
            df = read_csv(output_file, names=header, delimiter=',')

            return df

        return dfs[0]
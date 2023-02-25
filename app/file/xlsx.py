'''
module for writing to xlsx files
'''
from dataclasses import dataclass
from typing import Any, Optional
import xlsxwriter


@dataclass
class Cell:
    '''
    Cell describes an xlsx cell. It also allows a format to be applied.
    '''
    value: Optional[str | int | bool | float] = ''
    
    '''
    specifies the cells individual format. 
    This can be any format that has been added to the workbook.
    '''
    cell_format: Optional[xlsxwriter.workbook.Format] = None


class XLSXWriter():
    '''
    class for writing to an xlsx file. Wraps the xlsxwriter package to simplify things.
    '''

    def __init__(self, filename: str = 'groups.xlsx') -> None:
        self.__workbook = xlsxwriter.Workbook(filename)
        self.__sheets: dict[str, xlsxwriter.workbook.Worksheet] = {}
        self.__formatters: dict[str, xlsxwriter.workbook.Format] = {}

    def new_format(self, name, props) -> xlsxwriter.workbook.Format:
        '''
        adds a new format to the workbook. 
        This allows users to specify certain formats and 
        they will be added to the formatters dict for string based lookup.
        
        Only formats that have been added to the workbook can be applied to cells
        '''
        xlsx_format = self.__workbook.add_format(props)
        self.__formatters[name] = xlsx_format

        return xlsx_format

    def new_sheet(self, sheet_name: str):
        '''
        adds a new sheet to the workbook and stores a reference to it in the dictionary
        '''
        self.__sheets[sheet_name] = self.__workbook.add_worksheet(sheet_name)

    def write_sheet(self, sheet: str, table: list[list[Cell]]):
        '''
        writes data to a worksheet. This includes the header and the data. If the sheet doesn't exist, it will create it.
        '''
        if not self.__sheets.get(sheet):
            self.new_sheet(sheet)

        for i, row in enumerate(table):
            for j, field in enumerate(row):
                self.__sheets[sheet].write(
                    i, j, field.value, field.cell_format)

    def save(self):
        '''
        Saves the workbook and closes it. After this is called, the workbook must be open again before being written to
        '''
        self.__workbook.close()


def convert_to_cells(table: list[list[Any]]) -> list[list[Cell]]:
    '''
    converts 2d lists to a table with cells
    '''
    table_cells: list[list[Cell]] = []
    for row in table:
        table_row = []
        for cell in row:
            table_row.append(Cell(cell))
        table_cells.append(table_row)

    return table_cells

'''
module for writing to xlsx files
'''
import xlsxwriter


class XLSXWriter():
    '''
    class for writing to an xlsx file. Wraps the xlsxwriter package to simplify things.
    '''

    def __init__(self, filename: str = 'groups.xlsx') -> None:
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.sheets: dict[str, xlsxwriter.workbook.Worksheet] = {}

    def new_sheet(self, sheet_name: str):
        '''
        adds a new sheet to the workbook and stores a reference to it in the dictionary
        '''
        self.sheets[sheet_name] = self.workbook.add_worksheet(sheet_name)

    def write_sheet(self, sheet: str, table: list[list]):
        '''
        writes data to a worksheet. This includes the header and the data. If the sheet doesn't exist, it will create it.
        '''
        if not self.sheets.get(sheet):
            self.new_sheet(sheet)

        for i, row in enumerate(table):
            for j, field in enumerate(row):
                self.sheets[sheet].write(i, j, field)

    def save(self):
        '''
        Saves the workbook and closes it. After this is called, the workbook must be open again before being written to
        '''
        self.workbook.close()

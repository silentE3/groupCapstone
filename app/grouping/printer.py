'''
This module contains a class for maintaining clean console output when writing (overwriting)
    a single console line continually during the grouping process.
'''


class GroupingConsolePrinter:
    '''
       Class for maintaining clean console output when  writing (overwriting) a
           single line continually during the grouping process.
       '''

    def __init__(self):
        self.prev_line_length = 0

    def print(self, text: str):
        '''
        Print 'text' via the 'print()' function to the console output, but
        ensuring that it overwrites the previously printed line entirely and
        with a carriage return rather than new line (in preparation for the line
        to be subsequently overwritten).
        '''
        input_text_length: int = len(text)
        new_line_length: int = max(
            input_text_length, self.prev_line_length)
        text = text.ljust(new_line_length)
        self.prev_line_length = input_text_length
        print(text, end='\r', flush=True)

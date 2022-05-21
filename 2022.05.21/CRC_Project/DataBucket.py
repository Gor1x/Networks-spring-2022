from random import randrange

from Crc import Crc


class DataBucket:
    _DEFAULT_CRC_POLYNOMIAL = '1011110100101010'

    def __init__(self, data_string, polynomial=None):
        if polynomial is None:
            polynomial = self._DEFAULT_CRC_POLYNOMIAL
        self.polynomial = polynomial
        self.data_string = data_string
        self.remainder = Crc(data_string, self.polynomial).get_remainder('0')

    def make_random_mistake(self):
        length = len(self.data_string)
        pos = randrange(0, length)
        data = list(self.data_string)
        if data[pos] == '1':
            data[pos] = '0'
        else:
            data[pos] = '1'
        self.data_string = "".join(data)

    def data_is_correct(self):
        return Crc(self.data_string, self.polynomial).is_correct(self.remainder)

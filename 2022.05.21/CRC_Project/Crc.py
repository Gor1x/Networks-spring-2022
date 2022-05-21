class Crc:
    def __init__(self, input_bitstring, polynomial_bitstring='1101'):
        self.checkCorrect(input_bitstring)
        self.checkCorrect(polynomial_bitstring)
        self.input = input_bitstring
        self.poly = polynomial_bitstring

    def _get_input_padded_array(self, padding, poly, len_input):
        input_padded = list(self.input + padding)
        while '1' in input_padded[:len_input]:
            cur_shift = input_padded.index('1')
            for i in range(len(poly)):
                input_padded[cur_shift + i] = str(int(poly[i] != input_padded[cur_shift + i]))
        return input_padded

    def get_remainder(self, initial_filler='0'):
        poly = self.poly.lstrip('0')
        len_input = len(self.input)
        padding = (len(poly) - 1) * initial_filler
        input_padded = self._get_input_padded_array(padding, poly, len_input)
        return ''.join(input_padded)[len_input:]

    def is_correct(self, check_value):
        poly = self.poly.lstrip('0')
        len_input = len(self.input)
        input_padded_array = self._get_input_padded_array(check_value, poly, len_input)
        return '1' not in ''.join(input_padded_array)[len_input:]

    @staticmethod
    def checkCorrect(input_bitstring):
        for c in input_bitstring:
            if c != '1' and c != '0':
                raise Exception(f'Bad argument {input_bitstring}')

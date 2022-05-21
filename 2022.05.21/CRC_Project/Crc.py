class Crc:
    def __init__(self, input_bitstring, polynomial_bitstring='1101'):
        self.checkCorrect(input_bitstring)
        self.checkCorrect(polynomial_bitstring)
        self.input_bitstring = input_bitstring
        self.polynomial_bitstring = polynomial_bitstring

    def _get_input_padded_array(self, initial_padding, polynomial_bitstring, len_input):
        input_padded_array = list(self.input_bitstring + initial_padding)
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] \
                    = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
        return input_padded_array

    def get_remainder(self, initial_filler='0'):
        """Calculate the CRC remainder of a string of bits using a chosen polynomial.
        initial_filler should be '1' or '0'.
        """
        polynomial_bitstring = self.polynomial_bitstring.lstrip('0')
        len_input = len(self.input_bitstring)
        initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
        input_padded_array = self._get_input_padded_array(initial_padding, polynomial_bitstring, len_input)
        return ''.join(input_padded_array)[len_input:]

    def is_correct(self, check_value):
        """Calculate the CRC check of a string of bits using a chosen polynomial."""
        polynomial_bitstring = self.polynomial_bitstring.lstrip('0')
        len_input = len(self.input_bitstring)
        initial_padding = check_value
        input_padded_array = self._get_input_padded_array(initial_padding, polynomial_bitstring, len_input)
        return '1' not in ''.join(input_padded_array)[len_input:]

    @staticmethod
    def checkCorrect(input_bitstring):
        for c in input_bitstring:
            if c != '1' and c != '0':
                raise Exception(f'Bad argument {input_bitstring}')

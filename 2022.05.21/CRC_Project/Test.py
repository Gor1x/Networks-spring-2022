import unittest
import random

from DataBucket import DataBucket


class Correct_NoMistakes_DifferentData(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(1337)

    def test_correct_without_mistakes1(self):
        bucket = DataBucket('101010100101010101110101010101010')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes2(self):
        bucket = DataBucket('1010101010')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes3(self):
        bucket = DataBucket('10101010101010')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes4(self):
        bucket = DataBucket('1010101011100011')
        self.assertTrue(bucket.data_is_correct())


class Correct_NoMistakes_DifferentPolynomial(unittest.TestCase):
    DEFAULT_DATA = '101010100101010101110101010101010'

    def setUp(self) -> None:
        random.seed(1337)

    def test_correct_without_mistakes1(self):
        bucket = DataBucket(self.DEFAULT_DATA, '1010')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes2(self):
        bucket = DataBucket(self.DEFAULT_DATA, '1')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes3(self):
        bucket = DataBucket(self.DEFAULT_DATA, '111')
        self.assertTrue(bucket.data_is_correct())

    def test_correct_without_mistakes4(self):
        bucket = DataBucket(self.DEFAULT_DATA, '101')
        self.assertTrue(bucket.data_is_correct())


class NotCorrect_WithMistakes(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(1337)

    def test_correct_without_mistakes1(self):
        bucket = DataBucket('1101')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes2(self):
        bucket = DataBucket('1010101010')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes3(self):
        bucket = DataBucket('10101010101010')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes4(self):
        bucket = DataBucket('1010101011100011')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())


class NotCorrect_WithMistakes_DifferentPolynomial(unittest.TestCase):
    DEFAULT_DATA = '101110101001'

    def setUp(self) -> None:
        random.seed(1337)

    def test_correct_without_mistakes1(self):
        bucket = DataBucket(self.DEFAULT_DATA, '1010')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes2(self):
        bucket = DataBucket(self.DEFAULT_DATA, '11010')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes3(self):
        bucket = DataBucket(self.DEFAULT_DATA, '111')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())

    def test_correct_without_mistakes4(self):
        bucket = DataBucket(self.DEFAULT_DATA, '101')
        bucket.make_random_mistake()
        self.assertFalse(bucket.data_is_correct())


if __name__ == '__main__':
    unittest.main()

import unittest
import homework02
import sys


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.allcondition = [[], ['input2.tx'], ['/p', 'input2.txt'], ['/p', '/p', 'input2.txt'], ['/p', '/p', '/p', 'input2.txt'], ['input2.txt'], ['/h', 'input2.txt'], ['/v', 'input2.txt'], ['/a', 'input2.txt'], ['/h', '/v', 'input2.txt'], ['/h', '/v', '/a', 'input2.txt']]     # 所有参数情况

    def test_wrong_args(self):
        for i in range(0, 5):
            sys.argv[1:] = self.allcondition[i]
            if i in [0, 2, 3, 4]:
                self.assertRaises(ValueError, homework02.main)
            elif i == 1:
                self.assertRaises(IOError, homework02.main)
            homework02.resetall()

    def test_zero_arg(self):
        sys.argv[1:] = self.allcondition[5]
        self.assertEqual(homework02.main(), 28)
        homework02.resetall()

    def test_one_arg(self):
        for i in range(6, 9):
            sys.argv[1:] = self.allcondition[i]
            if i == 6:
                self.assertEqual(homework02.main(), 34)
            elif i == 7:
                self.assertEqual(homework02.main(), 45)
            elif i == 8:
                self.assertEqual(homework02.main(), 50)
            homework02.resetall()

    def test_two_args(self):
        sys.argv[1:] = self.allcondition[9]
        self.assertEqual(homework02.main(), 49)
        homework02.resetall()

    def test_three_args(self):
        sys.argv[1:] = self.allcondition[10]
        self.assertEqual(homework02.main(), 54)
        homework02.resetall()


if __name__ == '__main__':
    unittest.main()

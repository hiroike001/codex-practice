"""数秘術ツールのテスト。実行: python3 -m unittest tools/test_numerology.py"""

import unittest
from datetime import date

from numerology import (
    birthday_number,
    calculate,
    life_path_all_digits,
    life_path_separate,
    parse_date,
    reduce_number,
)


class ReduceNumberTest(unittest.TestCase):
    def test_single_digit_stays(self):
        self.assertEqual(reduce_number(7), 7)

    def test_reduces_to_single_digit(self):
        self.assertEqual(reduce_number(38), 11)  # 3+8=11 → マスターで止まる
        self.assertEqual(reduce_number(29), 11)  # 2+9=11
        self.assertEqual(reduce_number(19), 1)  # 1+9=10 → 1

    def test_master_numbers_kept(self):
        for n in (11, 22, 33):
            self.assertEqual(reduce_number(n), n)


class LifePathTest(unittest.TestCase):
    def test_all_digits(self):
        # 1+9+8+0+0+1+0+1 = 20 → 2
        self.assertEqual(life_path_all_digits(date(1980, 1, 1)), 2)
        # 1+9+7+6+0+5+2+3 = 33（マスター）
        self.assertEqual(life_path_all_digits(date(1976, 5, 23)), 33)
        # 1+9+9+0+1+2+3+1 = 26 → 8
        self.assertEqual(life_path_all_digits(date(1990, 12, 31)), 8)

    def test_separate(self):
        # 年 1976 → 23 → 5、月 5、日 23 → 5 → 5+5+5 = 15 → 6
        self.assertEqual(life_path_separate(date(1976, 5, 23)), 6)
        # 年 1980 → 18 → 9、月 1、日 1 → 11 → 2
        self.assertEqual(life_path_separate(date(1980, 1, 1)), 11)

    def test_methods_can_differ(self):
        d = date(1976, 5, 23)
        self.assertNotEqual(life_path_all_digits(d), life_path_separate(d))


class BirthdayNumberTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(birthday_number(date(2000, 1, 9)), 9)
        self.assertEqual(birthday_number(date(2000, 1, 11)), 11)
        self.assertEqual(birthday_number(date(2000, 1, 22)), 22)
        self.assertEqual(birthday_number(date(2000, 1, 29)), 11)
        self.assertEqual(birthday_number(date(2000, 1, 30)), 3)


class ParseAndCalculateTest(unittest.TestCase):
    def test_parse_formats(self):
        self.assertEqual(parse_date("1976-05-23"), date(1976, 5, 23))
        self.assertEqual(parse_date("19760523"), date(1976, 5, 23))
        self.assertEqual(parse_date("1976/5/23"), date(1976, 5, 23))

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            parse_date("1976-02-30")

    def test_calculate(self):
        r = calculate(date(1976, 5, 23))
        self.assertEqual(r.life_path, 33)
        self.assertTrue(r.is_master)
        self.assertEqual(r.birthday_number, 5)


if __name__ == "__main__":
    unittest.main()

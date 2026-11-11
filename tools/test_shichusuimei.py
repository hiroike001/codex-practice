"""四柱推命ツールのテスト。実行: cd tools && python3 -m unittest test_shichusuimei.py

検算用の日付は、万年暦サイト（wannianli.tianqi.com）の記載で確認したもの。
"""

import unittest
from datetime import date, timedelta

from shichusuimei import DAY_MASTER_TYPES, calculate, day_pillar, parse_date


class DayPillarTest(unittest.TestCase):
    def test_known_dates(self):
        # 万年暦サイトの記載と一致を確認した日付
        self.assertEqual(day_pillar(date(2000, 1, 1)), "戊午")
        self.assertEqual(day_pillar(date(2026, 1, 17)), "辛卯")
        self.assertEqual(day_pillar(date(2026, 1, 31)), "乙巳")
        self.assertEqual(day_pillar(date(2026, 2, 1)), "丙午")

    def test_sixty_day_cycle(self):
        d = date(1976, 5, 23)
        self.assertEqual(day_pillar(d), day_pillar(d + timedelta(days=60)))
        self.assertNotEqual(day_pillar(d), day_pillar(d + timedelta(days=1)))

    def test_consecutive_days_advance_by_one(self):
        stems = "甲乙丙丁戊己庚辛壬癸"
        d = date(1980, 3, 1)
        a, b = day_pillar(d)[0], day_pillar(d + timedelta(days=1))[0]
        self.assertEqual((stems.index(a) + 1) % 10, stems.index(b))


class CalculateTest(unittest.TestCase):
    def test_type_name(self):
        r = calculate(date(2000, 1, 1))
        self.assertEqual(r.day_stem, "戊")
        self.assertEqual(r.type_name, "山タイプ")

    def test_all_ten_types_defined(self):
        self.assertEqual(len(DAY_MASTER_TYPES), 10)

    def test_parse(self):
        self.assertEqual(parse_date("1976/5/23"), date(1976, 5, 23))
        self.assertEqual(parse_date("19760523"), date(1976, 5, 23))
        with self.assertRaises(ValueError):
            parse_date("1976-13-01")


if __name__ == "__main__":
    unittest.main()

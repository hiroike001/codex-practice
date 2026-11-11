"""四柱推命の計算ツール（ハイロー用）— 日柱と「生まれ日のタイプ」

生年月日から、生まれた日の干支（日柱）を出し、日干（生まれ日のタイプ）を10タイプで返す。

計算方法:
    日の干支は60日でひと回りする。ユリウス通日（JDN）を使い、
    index = (JDN + 49) mod 60 （0 = 甲子）で求める。
    検算: 2000-01-01 = 戊午、1900-01-01 = 甲戌（万年暦サイトの記載と一致を確認済み）

このツールでまだ扱っていないこと（未実装）:
    - 年柱・月柱：節入り（二十四節気の切り替わり時刻）の計算が必要
    - 時柱：生まれた時刻が必要
    - 大運（10年ごとの運の流れ）：月柱と節入りが必要
    - 23時台に生まれた人：流派によって翌日の干支として扱う場合がある。
      このツールは 0 時で日付を切り替える

使い方:
    python3 tools/shichusuimei.py 1976-05-23
    python3 tools/shichusuimei.py 1976-05-23 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

# 投稿で使う、わかりやすい呼び名（専門用語を使わないため）
DAY_MASTER_TYPES = {
    "甲": {"type_name": "大樹タイプ", "reading": "きのえ", "element": "木", "image": "まっすぐ伸びる大きな木"},
    "乙": {"type_name": "草花タイプ", "reading": "きのと", "element": "木", "image": "しなやかに咲く草花"},
    "丙": {"type_name": "太陽タイプ", "reading": "ひのえ", "element": "火", "image": "周りを照らす太陽"},
    "丁": {"type_name": "灯火タイプ", "reading": "ひのと", "element": "火", "image": "暗い場所をあたためる灯り"},
    "戊": {"type_name": "山タイプ", "reading": "つちのえ", "element": "土", "image": "どっしり構える山"},
    "己": {"type_name": "大地タイプ", "reading": "つちのと", "element": "土", "image": "作物を育てる畑の土"},
    "庚": {"type_name": "鋼タイプ", "reading": "かのえ", "element": "金", "image": "強くてまっすぐな鋼"},
    "辛": {"type_name": "宝石タイプ", "reading": "かのと", "element": "金", "image": "磨かれて光る宝石"},
    "壬": {"type_name": "大海タイプ", "reading": "みずのえ", "element": "水", "image": "広く流れる海や大河"},
    "癸": {"type_name": "雨露タイプ", "reading": "みずのと", "element": "水", "image": "静かにしみこむ雨や露"},
}

JDN_OFFSET = 1721425  # date.toordinal() + JDN_OFFSET = ユリウス通日（正午基準の整数）


def julian_day_number(d: date) -> int:
    return d.toordinal() + JDN_OFFSET


def sexagenary_index(d: date) -> int:
    """日の干支の番号（0 = 甲子 〜 59 = 癸亥）。"""
    return (julian_day_number(d) + 49) % 60


def day_pillar(d: date) -> str:
    i = sexagenary_index(d)
    return STEMS[i % 10] + BRANCHES[i % 12]


@dataclass
class DayMasterResult:
    birthday: str
    day_pillar: str
    day_stem: str
    type_name: str
    reading: str
    element: str
    image: str


def calculate(birthday: date) -> DayMasterResult:
    pillar = day_pillar(birthday)
    stem = pillar[0]
    info = DAY_MASTER_TYPES[stem]
    return DayMasterResult(birthday=birthday.isoformat(), day_pillar=pillar, day_stem=stem, **info)


def parse_date(text: str) -> date:
    cleaned = text.strip().replace("/", "-").replace(".", "-")
    if cleaned.isdigit() and len(cleaned) == 8:
        return date(int(cleaned[:4]), int(cleaned[4:6]), int(cleaned[6:]))
    parts = cleaned.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"invalid date: {text}")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="四柱推命：生まれ日のタイプ（日干）を出す")
    parser.add_argument("birthday", help="生年月日（例: 1976-05-23 / 1976/5/23 / 19760523）")
    parser.add_argument("--json", action="store_true", help="JSON で出力する")
    args = parser.parse_args(argv)

    try:
        birthday = parse_date(args.birthday)
    except ValueError:
        print(f"生年月日の形式が読めません: {args.birthday}（例: 1976-05-23、1976/5/23、19760523）", file=sys.stderr)
        return 2

    r = calculate(birthday)
    if args.json:
        print(json.dumps(asdict(r), ensure_ascii=False))
    else:
        print(f"生年月日: {r.birthday}")
        print(f"生まれ日のタイプ: {r.type_name}（{r.image}）")
        print(f"専門用語: 日干={r.day_stem}（{r.reading}）、日柱={r.day_pillar}、五行={r.element}")
        print("※23時台生まれの人は、流派によって翌日のタイプになることがあります")
    return 0


if __name__ == "__main__":
    sys.exit(main())

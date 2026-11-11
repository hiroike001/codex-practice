"""数秘術の計算ツール（ハイロー用）

生年月日から次の数字を計算する。

- 運命数（ライフパスナンバー）：生年月日の数字をすべて足し、1桁になるまで足し続ける。
  途中で 11・22・33 になった場合は、そこで止める（マスターナンバー）。
- 誕生数（バースデーナンバー）：生まれた「日」の数字を1桁になるまで足す。
  11・22 はマスターナンバーとして残す。

計算方法には流派による違いがある。このツールの既定は「全部の数字を足す」方式。
年・月・日をそれぞれ1桁にしてから足す方式も `--method separate` で選べる。
2つの方式は、マスターナンバーが出るかどうかで結果が変わることがある。

使い方:
    python3 tools/numerology.py 1976-05-23
    python3 tools/numerology.py 1976-05-23 --method separate
    python3 tools/numerology.py 1976-05-23 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date

MASTER_NUMBERS = (11, 22, 33)


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))


def reduce_number(n: int, keep_master: tuple[int, ...] = MASTER_NUMBERS) -> int:
    """1桁になるまで各桁を足す。keep_master に含まれる数になったら止める。"""
    while n > 9 and n not in keep_master:
        n = digit_sum(n)
    return n


def life_path_all_digits(birthday: date) -> int:
    """全部の数字を足す方式。例: 1976-05-23 → 1+9+7+6+0+5+2+3 = 33"""
    total = digit_sum(int(birthday.strftime("%Y%m%d")))
    return reduce_number(total)


def life_path_separate(birthday: date) -> int:
    """年・月・日をそれぞれ1桁（またはマスターナンバー）にしてから足す方式。"""
    parts = [reduce_number(x) for x in (birthday.year, birthday.month, birthday.day)]
    return reduce_number(sum(parts))


def birthday_number(birthday: date) -> int:
    """生まれた日の数字を1桁にする（11・22 は残す）。"""
    return reduce_number(birthday.day, keep_master=(11, 22))


@dataclass
class NumerologyResult:
    birthday: str
    method: str
    life_path: int
    birthday_number: int
    is_master: bool


def calculate(birthday: date, method: str = "all") -> NumerologyResult:
    if method == "all":
        lp = life_path_all_digits(birthday)
    elif method == "separate":
        lp = life_path_separate(birthday)
    else:
        raise ValueError(f"unknown method: {method}")
    return NumerologyResult(
        birthday=birthday.isoformat(),
        method=method,
        life_path=lp,
        birthday_number=birthday_number(birthday),
        is_master=lp in MASTER_NUMBERS,
    )


def parse_date(text: str) -> date:
    cleaned = text.strip().replace("/", "-").replace(".", "-")
    if cleaned.isdigit() and len(cleaned) == 8:
        return date(int(cleaned[:4]), int(cleaned[4:6]), int(cleaned[6:]))
    parts = cleaned.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"invalid date: {text}")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="数秘術の計算（運命数・誕生数）")
    parser.add_argument("birthday", help="生年月日（例: 1976-05-23 / 1976/5/23 / 19760523）")
    parser.add_argument("--method", choices=["all", "separate"], default="all",
                        help="all=全部の数字を足す（既定） / separate=年・月・日を別々に1桁にしてから足す")
    parser.add_argument("--json", action="store_true", help="JSON で出力する")
    args = parser.parse_args(argv)

    try:
        birthday = parse_date(args.birthday)
    except ValueError:
        print(f"生年月日の形式が読めません: {args.birthday}（例: 1976-05-23、1976/5/23、19760523）", file=sys.stderr)
        return 2

    result = calculate(birthday, args.method)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        master = "（マスターナンバー）" if result.is_master else ""
        print(f"生年月日: {result.birthday}")
        print(f"運命数: {result.life_path}{master}")
        print(f"誕生数: {result.birthday_number}")
        print(f"計算方式: {'全部の数字を足す' if result.method == 'all' else '年・月・日を別々に足す'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
マンガ制作スタジオが出力した UTF-8 CSV を Shift-JIS に変換する。

使い方:
    python convert_sjis.py "コマ指示_P1.csv"
    python convert_sjis.py            # このフォルダの *.csv をまとめて変換

出力: 元のファイル名 + "_sjis.csv"（元ファイルは触らない）
Shift-JIS にない文字（①②③④ や ～ など）は近い文字に置き換える。
"""
import sys
import glob
import os

# Shift-JIS で化けやすい文字の置き換え表
REPLACE = {
    "①": "(1)", "②": "(2)", "③": "(3)", "④": "(4)", "⑤": "(5)",
    "⑥": "(6)", "⑦": "(7)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)",
    "～": "〜", "－": "-", "＂": '"', "≒": "≒",
}


def convert(path):
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()

    for a, b in REPLACE.items():
        text = text.replace(a, b)

    base, ext = os.path.splitext(path)
    out = base + "_sjis" + ext

    # 変換できない文字は "?" ではなく削らずに近似（errors="replace"）
    with open(out, "w", encoding="cp932", errors="replace", newline="") as f:
        f.write(text)

    print("変換しました: %s" % out)


def main():
    targets = sys.argv[1:]
    if not targets:
        targets = [p for p in glob.glob("*.csv") if not p.endswith("_sjis.csv")]

    if not targets:
        print("変換するCSVが見つかりません。")
        print('使い方: python convert_sjis.py "ファイル名.csv"')
        return

    for path in targets:
        if not os.path.exists(path):
            print("見つかりません: %s" % path)
            continue
        convert(path)


if __name__ == "__main__":
    main()

from __future__ import annotations

import concurrent

import tqdm
from generator.checker.constants import *
from generator.checker.dataclass import *
from generator.checker.errors import *
from generator.checker.function import *


def solve(board: Board, targets: set[str]):
    board.shuffle(targets)


def main():
    success = 0
    c_list = ElementList(HEIGHT, WIDTH, Attribute.C)
    p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)
    hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)
    vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)
    hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)
    vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)

    board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)
    targets = {"C", "Ep"}

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # まず Future のリストを作る
        futures = [
            executor.submit(solve, board, targets) for _ in range(NUMBER_OF_SAMPLES)
        ]

        # tqdmでプログレスバー表示
        with tqdm(total=len(futures)) as pbar:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                success += 1
                if CORRECT_RANGE[1] < success:
                    raise PanicError("成功回数が大きすぎました。")
                # ここで result を何らかの形で使ってもOK
                pbar.update(1)  # 1件完了したのでプログレスバーを進める


if __name__ == "__main__":
    main()

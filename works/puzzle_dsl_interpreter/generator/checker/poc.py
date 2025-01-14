from __future__ import annotations

import concurrent

import tqdm
from generator.checker.constants import *
from generator.checker.dataclass import *
from generator.checker.errors import *
from generator.checker.function import *


def solve(board: Board, targets: set[str]):
    board.shuffle(targets)

    def v3(zk: Element):
        def v8(l6: Element):
            v12 = board.b(Attribute.Ep)
            v11 = absolute_set(v12)
            v10 = int(WIDTH)  # mはWIDTHに変換
            v9 = int_value_comparison("!=", v10, v11)
            return v9

        v7 = board.b(Attribute.C)
        v6 = generation_set(v7, v8)
        v5 = board.b(Attribute.Ec)
        v4 = is_in(v5, v6)  # <-はis_in
        return v4

    v2 = board.b(Attribute.P)
    v1 = generation_set(v2, v3)
    return v1


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

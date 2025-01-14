from __future__ import annotations

import concurrent
import concurrent.futures
import sys

from generator.checker.constants import *
from generator.checker.dataclass import *
from generator.checker.errors import *
from generator.checker.function import *


def constraint0(board: Board) -> bool:
    v1 = board.b(Attribute.P)
    v2 = board.b(Attribute.Ep)
    v0 = is_in(v1, v2)
    return v0


def constraint1(board: Board) -> bool:
    v6 = board.b(Attribute.P)

    def v7(zk: Element):
        v9 = board.b(Attribute.Ec)
        v11 = board.b(Attribute.C)

        def v12(l6: Element):
            v14 = int(WIDTH)
            v17 = board.b(Attribute.Ep)
            v16 = int(absolute_set(v17))
            v15 = int(v16)
            v13 = int_value_comparison("!=", v14, v15)
            return v13

        v10 = generation_set(v11, v12)
        v8 = is_in(v9, v10)
        return v8

    v5 = generation_set(v6, v7)

    def v18(mr):
        v24 = cycle(mr)
        v23 = int(v24)
        v25 = 13
        v22 = int_operation("*", v23, v25)
        v21 = int(v22)
        v27 = solution(mr)
        v26 = int(v27)
        v20 = int_value_comparison("<", v21, v26)
        v29 = connect(mr, {Relationship.D})

        def v30(c):
            def v32(dd):
                v35 = all_different(dd)
                v34 = not_bool(v35)
                v40 = cross(dd)
                v39 = int(v40)
                v42 = cross(c)
                v41 = int(v42)
                v38 = int_value_comparison("!=", v39, v41)
                v44 = connect(dd, {Relationship.D, Relationship.H})
                v45 = connect(mr, {Relationship.V, Relationship.H})
                v43 = v44 == v45
                v37 = and_bool(v38, v43)
                v36 = not_bool(v37)
                v33 = then_bool(v34, v36)
                return v33

            v31 = is_all(mr, v32)
            return v31

        v28 = is_all(v29, v30)
        v19 = or_bool(v20, v28)
        return v19

    v4 = is_exists(v5, v18)
    v47 = board.b(Attribute.P)

    def v48(a):
        v51 = is_rectangle(a)
        v50 = not_bool(v51)
        v49 = not_bool(v50)
        return v49

    v46 = is_exists(v47, v48)
    v3 = then_bool(v4, v46)
    return v3


def solve(board: Board, targets: set[str]):
    try:
        board.shuffle(targets)
        for constraint in [constraint1, constraint0]:
            if not constraint(board):
                return 0
        return 1
    except Exception:
        raise PanicError


def main():
    success = 0
    c_list = ElementList(HEIGHT, WIDTH, Attribute.C)
    p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)
    hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)
    vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)
    hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)
    vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)
    board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)
    targets = {"Ep", "P", "C", "Ec"}

    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        futures = [
            executor.submit(solve, board, targets) for _ in range(NUMBER_OF_SAMPLES)
        ]
        try:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                success += result
                if CORRECT_RANGE[1] < success:
                    raise PanicError("成功回数が大きすぎました。")
        except PanicError as e:
            for future in futures:
                if not future.running():
                    future.cancel()
            for process in executor._processes.values():
                process.kill()
            executor.shutdown(wait=False, cancel_futures=True)
            sys.exit(1)


if __name__ == "__main__":
    main()

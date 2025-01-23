from __future__ import annotations

import concurrent.futures

from generator.checker.constants import *
from generator.checker.dataclass import *
from generator.checker.errors import *
from generator.checker.function import *


def constraint0(board: Board) -> bool:
    v2 = board.b(Attribute.Ec)

    def v3(r):
        v5 = connect(r, {Relationship.D})

        def v6(w):
            v8 = is_rectangle(w)
            v11 = cross(w)
            v10 = int(v11)
            v17 = cross(r)
            v16 = int(v17)
            v19 = solution(w)
            v18 = int(v19)
            v15 = int_operation("*", v16, v18)
            v14 = int(v15)
            v21 = cross(r)
            v20 = int(v21)
            v13 = int_operation("*", v14, v20)
            v12 = int(v13)
            v9 = int_value_comparison("!=", v10, v12)
            v7 = and_bool(v8, v9)
            return v7

        v4 = is_all(v5, v6)
        return v4

    v1 = is_exists(v2, v3)
    v25 = board.b(Attribute.C)
    v24 = int(absolute_set(v25))
    v23 = int(v24)
    v28 = board.b(Attribute.P)
    v27 = int(absolute_set(v28))
    v26 = int(v27)
    v22 = int_value_comparison("==", v23, v26)
    v0 = then_bool(v1, v22)
    return v0


def constraint1(board: Board) -> bool:
    v32 = board.b(Attribute.Ep)

    def v33(os: Element):
        v36 = int(WIDTH)
        v37 = int(WIDTH)
        v35 = int_value_comparison(">", v36, v37)
        v34 = not_bool(v35)
        return v34

    v31 = generation_set(v32, v33)

    def v38(o):
        v41 = cross(o)
        v40 = int(v41)
        v42 = int(HEIGHT)
        v39 = int_value_comparison("==", v40, v42)
        return v39

    v30 = is_all(v31, v38)
    v50 = 81
    v51 = int(WIDTH)
    v49 = int_operation("-", v50, v51)
    v48 = int(v49)
    v52 = int(HEIGHT)
    v47 = int_operation("-", v48, v52)
    v46 = int(v47)
    v55 = int(WIDTH)
    v56 = int(HEIGHT)
    v54 = int_operation("*", v55, v56)
    v53 = int(v54)
    v45 = int_operation("-", v46, v53)
    v44 = int(v45)
    v57 = 94
    v43 = int_value_comparison(">", v44, v57)
    v29 = equivalent_bool(v30, v43)
    return v29


def solve(board: Board, targets: set[str]):
    try:
        board.shuffle(targets)
        for constraint in [constraint0, constraint1]:
            if not constraint(board):
                return 0
        return 1
    except Exception:
        raise PanicError


def main():
    success = 0
    samples = 0
    c_list = ElementList(HEIGHT, WIDTH, Attribute.C)
    p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)
    hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)
    vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)
    hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)
    vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)
    board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)
    targets = {"Ep", "P", "C", "Ec"}
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(solve, board, targets) for _ in range(NUMBER_OF_SAMPLES)
        ]
        try:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                samples += 1
                success += result
                if (
                    float(samples * 10 / NUMBER_OF_SAMPLES) > 1 and success < 1
                ) or CORRECT_RANGE[1] < success:
                    raise PanicError("成功回数が大きすぎました。")
        except PanicError:
            for future in futures:
                if not future.running():
                    future.cancel()
            for process in executor._processes.values():
                process.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            sys.exit(1)
    print(success)


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from enum import StrEnum

from generator.checker.errors import PanicError
from generator.checker.render import (
    compound_boolean,
    int_convert,
    quantifier_boolean,
    set_comparison,
    set_equation,
)

# グローバルで変数名を生成するカウンタ
var_counter = 0
func_counter = 0
INDENT = "    "


# ノードタイプのEnum
class NodeType(StrEnum):
    BOOLEAN = "boolean"
    SET = "set"
    VALUE = "value"


class BooleanType(StrEnum):
    QUANTIFIER = "quantifier"
    COMPOUND = "compound"
    NOT = "not"
    ALL_DIFFERENT = "all_different"
    SET_EQUATION = "set_equation"
    SET_COMPARISON = "set_comparison"
    INT_VALUE_COMPARISON = "int_value_comparison"
    IS_SQUARE = "is_square"
    IS_RECTANGLE = "is_rectangle"


class SetType(StrEnum):
    GENERATION_SET = "generation_set"
    CONNECT = "connect"
    B = "B"


class ValueType(StrEnum):
    CYCLE = "cycle"
    CROSS = "cross"
    SOLUTION = "solution"
    ABSOLUTE_SET = "absolute_set"
    INT = "int"
    INT_OPERATION = "int_operation"


def gen_var_name() -> str:
    """
    連番で v0, v1, v2, ... のような変数名を生成する。
    """
    global var_counter
    name = f"v{var_counter}"
    var_counter += 1
    return name


def gen_func_name() -> str:
    """
    連番で constraint0, constraint2, constraint3, ... のような変数名を生成する。
    """
    global func_counter
    name = f"constraint{func_counter}"
    func_counter += 1
    return name


def reset_var():
    global var_counter
    global func_counter
    var_counter = 0
    func_counter = 0


def parse_node(node: dict | str, indent_level: int = 1) -> tuple[list[str], str]:
    """
    JSONノードを解析し、(コード行のリスト, 結果を保持する変数名) を返す。
    node の "type" などを見てサブハンドラを呼び出す。
    """
    if isinstance(node, str):
        if node == "None":
            return [], "{}"
        return [], node
    ntype = node.get("type")

    match ntype:
        case NodeType.BOOLEAN:
            return handle_boolean_node(node, indent_level)
        case NodeType.SET:
            return handle_set_node(node, indent_level)
        case NodeType.VALUE:
            return handle_value_node(node, indent_level)
        case _:
            raise PanicError(f"Unsupported types. {ntype}")


def handle_boolean_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "boolean" のノードを処理。
    """
    lines: list[str] = []
    var_name = gen_var_name()  # このノードの結果を格納する変数
    indent_str = INDENT * indent_level

    # boolean ノードの詳細
    bname = node.get("name")  # "quantifier", "compound", "not", "all_different", etc.
    props = node.get("properties", {})
    args = node.get("args", {})

    match bname:
        case BooleanType.QUANTIFIER:
            # 例: {"quantifier": "All", "variable": "dd", "universal_set": {...}}
            quantifier_type = props["quantifier"]  # "All", "Exists" など
            variable = props["variable"]  # 変数名 (dd 等)
            universal_set = props["universal_set"]  # セットノード

            # 1) universal set を parse

            set_lines, set_var = parse_node(universal_set, indent_level)
            lines.extend(set_lines)

            # 2) 条件式の部分(quantifierノードの "args")を関数として定義する
            func_name = gen_var_name()
            lines.append(f"{indent_str}def {func_name}({variable}):")

            # quantifierノードの args は boolean か compound かなど、さらに parse
            body_lines, body_var = parse_node(node["args"], indent_level + 1)
            lines.extend(body_lines)

            # 関数の return
            lines.append(INDENT * (indent_level + 1) + f"return {body_var}")

            # 3) quantifier_type に応じて is_all, is_exist を呼ぶ
            # var_name = is_all(set_var, func_name)
            lines.append(
                f"{indent_str}{quantifier_boolean(var_name, set_var, func_name, quantifier_type)}",
            )

        case BooleanType.COMPOUND:
            # properties: {"op": "=>", "&&", "||" など}
            op = props["op"]
            left_node = args.get("left")
            right_node = args.get("right")

            # left / right を再帰処理
            if left_node is not None:
                left_lines, left_var = parse_node(left_node, indent_level)
                lines.extend(left_lines)
            else:
                raise PanicError("Left node is None.")

            if right_node is not None:
                right_lines, right_var = parse_node(right_node, indent_level)
                lines.extend(right_lines)
            else:
                raise PanicError("Left node is None.")

            lines.append(
                f"{indent_str}{compound_boolean(var_name, left_var, right_var, op)}",
            )

        case BooleanType.NOT:
            # args: boolean node
            child_node = node["args"]
            child_lines, child_var = parse_node(child_node, indent_level)
            lines.extend(child_lines)
            lines.append(f"{indent_str}{var_name} = not_bool({child_var})")

        case BooleanType.ALL_DIFFERENT:
            # all_different(variable)
            variable = args.get("variable")
            lines.append(f"{indent_str}{var_name} = all_different({variable})")

        case BooleanType.SET_EQUATION:
            # set_equation("==", left, right)
            op_ = props["op"]
            left_node = args["left"]
            right_node = args["right"]

            left_lines, left_var = parse_node(left_node, indent_level)
            lines.extend(left_lines)

            right_lines, right_var = parse_node(right_node, indent_level)
            lines.extend(right_lines)

            lines.append(
                f"{indent_str}{set_equation(var_name, left_var, right_var, op_)}",
            )

        case BooleanType.SET_COMPARISON:
            op_ = props["op"]
            left_node = args["left"]
            right_node = args["right"]

            left_lines, left_var = parse_node(left_node, indent_level)
            lines.extend(left_lines)

            right_lines, right_var = parse_node(right_node, indent_level)
            lines.extend(right_lines)

            lines.append(
                f"{indent_str}{set_comparison(var_name, left_var, right_var, op_)}",
            )

        case BooleanType.INT_VALUE_COMPARISON:
            # int_value_comparison("!=", left, right)
            op_ = props["op"]
            left_node = args["left"]
            right_node = args["right"]

            left_lines, left_var = parse_node(left_node, indent_level)
            lines.extend(left_lines)

            right_lines, right_var = parse_node(right_node, indent_level)
            lines.extend(right_lines)

            lines.append(
                f'{indent_str}{var_name} = int_value_comparison("{op_}", {left_var}, {right_var})',
            )

        case BooleanType.IS_RECTANGLE:
            variable = args.get("variable")
            lines.append(f"{indent_str}{var_name} = is_rectangle({variable})")

        case BooleanType.IS_SQUARE:
            variable = args.get("variable")
            lines.append(f"{indent_str}{var_name} = is_square({variable})")

        case _:
            raise PanicError("Unsupported boolean")

    return lines, var_name


def handle_set_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "set" のノードを処理し、(コード行のリスト, 結果変数名) を返す。
    """
    lines: list[str] = []
    var_name = gen_var_name()
    indent_str = INDENT * indent_level

    sname = node["name"]  # "B", "connect", etc.
    args = node.get("args", {})
    props = node.get("properties", {})

    match sname:
        # 例に合わせた実装。必要に応じて拡張する。
        case SetType.B:
            struct = args.get("struct")
            if struct is None:
                raise PanicError("data doesn't have struct field.")
            lines.append(f"{indent_str}{var_name} = board.b(Attribute.{struct})")
        case SetType.CONNECT:
            # connect( variable, {Relationship.X, Relationship.Y, ...} )
            rels = set(args.get("relationship", []))
            child_var: str
            converted_rels = {f"Relationship.{r.replace("'", '')}" for r in rels}

            # variable が文字列ならそのまま、dict なら parse_node する
            variable_arg = args.get("variable")
            if isinstance(variable_arg, dict):
                # 再帰処理
                child_lines, child_var = parse_node(variable_arg, indent_level)
                lines.extend(child_lines)
            else:
                # 文字列(例: "dd")
                child_var = variable_arg

            lines.append(
                f"{indent_str}{var_name} = connect({child_var}, {converted_rels.__str__().replace("'", '')})",
            )
        case SetType.GENERATION_SET:
            variable_name = props["variable"]  # 例 "zk"

            # 1) universal_set を parse
            uni = props.get("universal_set")
            uni_lines, uni_var = parse_node(uni, indent_level)
            lines.extend(uni_lines)

            # 2) filter を parse → フィルタ用の関数を生成する
            fil = props.get("filter")
            func_name = gen_var_name()

            lines.append(f"{indent_str}def {func_name}({variable_name}: Element):")
            # フィルタ内部は boolean式をパースして「return <boolVar>」
            filter_lines, filter_var = parse_node(fil, indent_level + 1)
            lines.extend(filter_lines)
            lines.append(INDENT * (indent_level + 1) + f"return {filter_var}")

            # 3) 最後に generation_set(uni_var, func_name) を作る
            lines.append(
                f"{indent_str}{var_name} = generation_set({uni_var}, {func_name})",
            )

        case _:
            raise PanicError("Unsupported set type.")

    return lines, var_name


def handle_value_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "value" ノードを処理し、(コード行リスト, 結果変数名) を返す。
    """
    lines: list[str] = []
    var_name = gen_var_name()  # 例: v0, v1, ...
    indent_str = INDENT * indent_level

    vname = node.get("name")  # "int", "int_operation", "cross", "cycle", etc.
    args = node.get("args", {})

    match vname:
        case ValueType.INT:
            # "int" ノードの場合は、さらに "args": {"value": ...} がある
            val = args.get("value")

            if isinstance(val, dict):
                # ここが再帰ポイント: たとえば int_operation などを内包している
                sub_lines, sub_var = parse_node(val, indent_level)
                lines.extend(sub_lines)
                # "int(...)" でラップしたいなら:
                lines.append(f"{indent_str}{var_name} = int({sub_var})")
                # あるいは単に代入しておけばいいなら:
                # lines.append(f"{indent_str}{var_name} = {sub_var}")
            elif isinstance(val, str):
                # valが "13" や "m" などの文字列の場合
                lines.append(f"{indent_str}{var_name} = int({int_convert(val)})")

            else:
                raise PanicError("Unsupported int.")

        case ValueType.INT_OPERATION:
            # 例: "properties": {"op": "*"}, "args": {"left":{...}, "right":{...}}
            op_ = node.get("properties", {}).get("op")
            left_node = args.get("left")
            right_node = args.get("right")

            # left, right それぞれ再帰処理
            left_lines, left_var = parse_node(left_node, indent_level)
            lines.extend(left_lines)

            right_lines, right_var = parse_node(right_node, indent_level)
            lines.extend(right_lines)

            lines.append(
                f"{indent_str}{var_name} = int_operation('{op_}', {left_var}, {right_var})",
            )

        case ValueType.CYCLE:
            # 例: cycle(variable="mr")
            variable = args.get("variable")
            # ここでは「cycle(...) → intを返す関数」と想定
            lines.append(f"{indent_str}{var_name} = cycle({variable})")

        case ValueType.CROSS:
            # 例: cross(variable="dd") => int
            variable = args.get("variable")
            lines.append(f"{indent_str}{var_name} = cross({variable})")

        case ValueType.ABSOLUTE_SET:
            sub_lines, sub_var = parse_node(args, indent_level)
            lines.extend(sub_lines)
            # absolute_set(sub_var) を生成
            lines.append(f"{indent_str}{var_name} = int(absolute_set({sub_var}))")

        case ValueType.SOLUTION:
            variable = args.get("variable")
            lines.append(f"{indent_str}{var_name} = solution({variable})")

        case _:
            raise PanicError(f"Unsupported value type. {vname}")

    return lines, var_name


def generate_code(json_data: dict) -> str:
    """
    汎用的に JSON データをパースし、最終的に main() 関数の中で
    トップレベルの式を生成して return する Python コードを返す。
    """
    reset_var()
    lines = []
    lines.append("from __future__ import annotations")

    lines.append("import concurrent.futures")
    lines.append("import sys")
    lines.append("from generator.checker.constants import *")
    lines.append("from generator.checker.dataclass import *")
    lines.append("from generator.checker.errors import *")
    lines.append("from generator.checker.function import *")
    constraints = json_data["constraints"]
    targets_list = []
    func_lists = []
    for constraint in constraints:
        func_lines = []
        targets_list.extend(constraint["targets"])
        top_lines, top_var = parse_node(constraint["constraint"], 0)
        func_name = gen_func_name()
        func_lists.append((func_name, len(top_lines)))
        func_lines.append(f"def {func_name}(board: Board) -> bool:")
        for ln in top_lines:
            func_lines.append(INDENT + ln)
        func_lines.append(f"{INDENT}return {top_var}")

        lines.extend(func_lines)
    func_lists.sort(key=lambda x: x[1])
    sorted_func_lists = [x[0] for x in func_lists]
    targets = set(targets_list)

    # 最後にトップレベルの結果を return するなど好きに処理
    # ここでは「return 変数」にしておく
    # fmt: off


    lines.append("def solve(board: Board, targets: set[str]):")
    lines.append(f"{INDENT}try:")
    lines.append(f"{INDENT}{INDENT}board.shuffle(targets)")
    lines.append(f"{INDENT}{INDENT}for constraint in {sorted_func_lists.__str__().replace("'","")}:")
    lines.append(f"{INDENT}{INDENT}{INDENT}if not constraint(board):")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}return 0")
    lines.append(f"{INDENT}{INDENT}return 1")
    lines.append(f"{INDENT}except Exception:")
    lines.append(f"{INDENT}{INDENT}raise PanicError")
    lines.append("def main():")
    lines.append(f"{INDENT}success = 0")
    lines.append(f"{INDENT}samples = 0")
    lines.append(f"{INDENT}c_list = ElementList(HEIGHT, WIDTH, Attribute.C)")
    lines.append(f"{INDENT}p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)")
    lines.append(f"{INDENT}hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)")
    lines.append(f"{INDENT}vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)")
    lines.append(f"{INDENT}hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)")
    lines.append(f"{INDENT}vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)")
    lines.append(f"{INDENT}board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)")
    lines.append(f"{INDENT}targets = {targets.__str__()}")
    lines.append(f"{INDENT}with concurrent.futures.ProcessPoolExecutor() as executor:")
    lines.append(f"{INDENT}{INDENT}futures = [")
    lines.append(f"{INDENT}{INDENT}{INDENT}executor.submit(solve, board, targets) for _ in range(NUMBER_OF_SAMPLES)")
    lines.append(f"{INDENT}{INDENT}]")
    lines.append(f"{INDENT}{INDENT}try:")
    lines.append(f"{INDENT}{INDENT}{INDENT}for future in concurrent.futures.as_completed(futures):")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}result = future.result()")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}samples+=1")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}success += result")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}if float(samples * 10 / NUMBER_OF_SAMPLES) > 1 and success < 1:")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}print(f'試行回数: {{samples}}, 成功回数: {{success}}')")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}raise PanicError('成功回数が少なすぎました。')")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}if CORRECT_RANGE[1] < success:")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}print(f'試行回数: {{samples}}, 成功回数: {{success}}')")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}raise PanicError('成功回数が多すぎました。')")
    lines.append(f"{INDENT}{INDENT}except PanicError:")
    lines.append(f"{INDENT}{INDENT}{INDENT}for future in futures:")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}if not future.running():")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}future.cancel()")
    lines.append(f"{INDENT}{INDENT}{INDENT}for process in executor._processes.values():")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}process.cancel()")
    lines.append(f"{INDENT}{INDENT}{INDENT}executor.shutdown(wait=False, cancel_futures=True)")
    lines.append(f"{INDENT}{INDENT}{INDENT}sys.exit(1)")
    lines.append(f"{INDENT}print(success)")

    lines.append('if __name__ == "__main__":')
    lines.append(f"{INDENT}main()")
    # fmt: on

    # 全体を結合して完成
    return "\n".join(lines)


if __name__ == "__main__":
    # ------------------------------------------------------------
    # 例: 質問文で提示された JSON (quantifier がトップレベル)
    # ------------------------------------------------------------
    json_str1 = r"""
{
    "structs": [],
    "domain": [
        {
            "name": "P",
            "domain": [
                "null",
                "45"
            ],
            "hidden": [
                "n",
                "undecided"
            ]
        },
        {
            "name": "C",
            "domain": [
                "null",
                "m"
            ],
            "hidden": [
                "null",
                "undecided"
            ]
        },
        {
            "name": "Ep",
            "domain": [
                "null",
                "null"
            ],
            "hidden": [
                "8",
                "undecided",
                "n"
            ]
        },
        {
            "name": "Ec",
            "domain": [
                "null",
                "m",
                "1"
            ],
            "hidden": [
                "undecided",
                "undecided",
                "m"
            ]
        }
    ],
    "constraints": [
        {
            "targets": [
                "P",
                "Ep"
            ],
            "constraint": {
                "type": "boolean",
                "name": "set_comparison",
                "properties": {
                    "op": "<-"
                },
                "args": {
                    "left": {
                        "type": "set",
                        "name": "B",
                        "args": {
                            "struct": "P"
                        }
                    },
                    "right": {
                        "type": "set",
                        "name": "B",
                        "args": {
                            "struct": "Ep"
                        }
                    }
                }
            }
        },
        {
            "targets": [
                "Ec",
                "P",
                "C",
                "Ep"
            ],
            "constraint": {
                "type": "boolean",
                "name": "compound",
                "properties": {
                    "op": "=>"
                },
                "args": {
                    "right": {
                        "type": "boolean",
                        "name": "quantifier",
                        "properties": {
                            "quantifier": "Exists",
                            "variable": "a",
                            "universal_set": {
                                "type": "set",
                                "name": "B",
                                "args": {
                                    "struct": "P"
                                }
                            }
                        },
                        "args": {
                            "type": "boolean",
                            "name": "not",
                            "args": {
                                "type": "boolean",
                                "name": "not",
                                "args": {
                                    "type": "boolean",
                                    "name": "is_rectangle",
                                    "args": {
                                        "variable": "a"
                                    }
                                }
                            }
                        }
                    },
                    "left": {
                        "type": "boolean",
                        "name": "quantifier",
                        "properties": {
                            "quantifier": "Exists",
                            "variable": "mr",
                            "universal_set": {
                                "type": "set",
                                "name": "generation_set",
                                "properties": {
                                    "variable": "zk",
                                    "universal_set": {
                                        "type": "set",
                                        "name": "B",
                                        "args": {
                                            "struct": "P"
                                        }
                                    },
                                    "filter": {
                                        "type": "boolean",
                                        "name": "set_comparison",
                                        "properties": {
                                            "op": "<-"
                                        },
                                        "args": {
                                            "left": {
                                                "type": "set",
                                                "name": "B",
                                                "args": {
                                                    "struct": "Ec"
                                                }
                                            },
                                            "right": {
                                                "type": "set",
                                                "name": "generation_set",
                                                "properties": {
                                                    "variable": "l6",
                                                    "universal_set": {
                                                        "type": "set",
                                                        "name": "B",
                                                        "args": {
                                                            "struct": "C"
                                                        }
                                                    },
                                                    "filter": {
                                                        "type": "boolean",
                                                        "name": "int_value_comparison",
                                                        "properties": {
                                                            "op": "!="
                                                        },
                                                        "args": {
                                                            "left": {
                                                                "type": "value",
                                                                "name": "int",
                                                                "args": {
                                                                    "value": "m"
                                                                }
                                                            },
                                                            "right": {
                                                                "type": "value",
                                                                "name": "int",
                                                                "args": {
                                                                    "value": {
                                                                        "type": "value",
                                                                        "name": "absolute_set",
                                                                        "args": {
                                                                            "type": "set",
                                                                            "name": "B",
                                                                            "args": {
                                                                                "struct": "Ep"
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "args": {
                            "type": "boolean",
                            "name": "compound",
                            "properties": {
                                "op": "||"
                            },
                            "args": {
                                "right": {
                                    "type": "boolean",
                                    "name": "quantifier",
                                    "properties": {
                                        "quantifier": "All",
                                        "variable": "c",
                                        "universal_set": {
                                            "type": "set",
                                            "name": "connect",
                                            "args": {
                                                "variable": "mr",
                                                "relationship": [
                                                    "D"
                                                ]
                                            }
                                        }
                                    },
                                    "args": {
                                        "type": "boolean",
                                        "name": "quantifier",
                                        "properties": {
                                            "quantifier": "All",
                                            "variable": "dd",
                                            "universal_set": "mr"
                                        },
                                        "args": {
                                            "type": "boolean",
                                            "name": "compound",
                                            "properties": {
                                                "op": "=>"
                                            },
                                            "args": {
                                                "right": {
                                                    "type": "boolean",
                                                    "name": "not",
                                                    "args": {
                                                        "type": "boolean",
                                                        "name": "compound",
                                                        "properties": {
                                                            "op": "&&"
                                                        },
                                                        "args": {
                                                            "right": {
                                                                "type": "boolean",
                                                                "name": "set_equation",
                                                                "properties": {
                                                                    "op": "=="
                                                                },
                                                                "args": {
                                                                    "left": {
                                                                        "type": "set",
                                                                        "name": "connect",
                                                                        "args": {
                                                                            "variable": "dd",
                                                                            "relationship": [
                                                                                "D",
                                                                                "H"
                                                                            ]
                                                                        }
                                                                    },
                                                                    "right": {
                                                                        "type": "set",
                                                                        "name": "connect",
                                                                        "args": {
                                                                            "variable": "mr",
                                                                            "relationship": [
                                                                                "H",
                                                                                "V"
                                                                            ]
                                                                        }
                                                                    }
                                                                }
                                                            },
                                                            "left": {
                                                                "type": "boolean",
                                                                "name": "int_value_comparison",
                                                                "properties": {
                                                                    "op": "!="
                                                                },
                                                                "args": {
                                                                    "left": {
                                                                        "type": "value",
                                                                        "name": "int",
                                                                        "args": {
                                                                            "value": {
                                                                                "type": "value",
                                                                                "name": "cross",
                                                                                "args": {
                                                                                    "variable": "dd"
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    "right": {
                                                                        "type": "value",
                                                                        "name": "int",
                                                                        "args": {
                                                                            "value": {
                                                                                "type": "value",
                                                                                "name": "cross",
                                                                                "args": {
                                                                                    "variable": "c"
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                },
                                                "left": {
                                                    "type": "boolean",
                                                    "name": "not",
                                                    "args": {
                                                        "type": "boolean",
                                                        "name": "all_different",
                                                        "args": {
                                                            "variable": "dd"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "left": {
                                    "type": "boolean",
                                    "name": "int_value_comparison",
                                    "properties": {
                                        "op": "<"
                                    },
                                    "args": {
                                        "left": {
                                            "type": "value",
                                            "name": "int",
                                            "args": {
                                                "value": {
                                                    "type": "value",
                                                    "name": "int_operation",
                                                    "properties": {
                                                        "op": "*"
                                                    },
                                                    "args": {
                                                        "left": {
                                                            "type": "value",
                                                            "name": "int",
                                                            "args": {
                                                                "value": {
                                                                    "type": "value",
                                                                    "name": "cycle",
                                                                    "args": {
                                                                        "variable": "mr"
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        "right": {
                                                            "type": "value",
                                                            "name": "int",
                                                            "args": {
                                                                "value": "13"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "right": {
                                            "type": "value",
                                            "name": "int",
                                            "args": {
                                                "value": {
                                                    "type": "value",
                                                    "name": "solution",
                                                    "args": {
                                                        "variable": "mr"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
}

"""
    data1 = json.loads(json_str1)
    code1 = generate_code(data1)
    print("=== Example 1: Top-level is quantifier ===")
    print(code1)
    print()

from __future__ import annotations

import json
from enum import StrEnum

from generator.checker.errors import PanicError
from generator.checker.render import compound_boolean

# グローバルで変数名を生成するカウンタ
var_counter = 0
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


def gen_var_name() -> str:
    """
    連番で v0, v1, v2, ... のような変数名を生成する。
    """
    global var_counter
    name = f"v{var_counter}"
    var_counter += 1
    return name


def parse_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    JSONノードを解析し、(コード行のリスト, 結果を保持する変数名) を返す。
    node の "type" などを見てサブハンドラを呼び出す。
    """
    ntype = node.get("type")

    match ntype:
        case NodeType.BOOLEAN:
            return handle_boolean_node(node, indent_level)
        case NodeType.SET:
            return handle_set_node(node, indent_level)
        case NodeType.VALUE:
            return handle_value_node(node, indent_level)
        case _:
            raise PanicError("Unsupported types.")


def handle_boolean_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "boolean" のノードを処理。
    """
    lines: list[str] = []
    var_name = gen_var_name()  # このノードの結果を格納する変数
    indent_str = "    " * indent_level

    # boolean ノードの詳細
    bname = node.get("name")  # "quantifier", "compound", "not", "all_different", etc.
    props = node.get("properties", {})
    args = node.get("args", {})

    if bname == BooleanType.QUANTIFIER:
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
        lines.append("    " * (indent_level + 1) + f"return {body_var}")

        # 3) quantifier_type に応じて is_all, is_exist を呼ぶ
        # var_name = is_all(set_var, func_name)
        if quantifier_type == "All":
            lines.append(f"{indent_str}{var_name} = is_all({set_var}, {func_name})")
        elif quantifier_type == "Exists":
            lines.append(f"{indent_str}{var_name} = is_exist({set_var}, {func_name})")
        else:
            raise PanicError("Unsupported quantifier.")

    elif bname == BooleanType.COMPOUND:
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

    elif bname == BooleanType.NOT:
        # args: boolean node
        child_node = node["args"]
        child_lines, child_var = parse_node(child_node, indent_level)
        lines.extend(child_lines)
        lines.append(f"{indent_str}{var_name} = _not({child_var})")

    elif bname == BooleanType.ALL_DIFFERENT:
        # all_different(variable)
        variable = args.get("variable")
        lines.append(f"{indent_str}{var_name} = all_different({variable})")

    elif bname == BooleanType.SET_EQUATION:
        # set_equation("==", left, right)
        op_ = props["op"]
        left_node = args["left"]
        right_node = args["right"]

        left_lines, left_var = parse_node(left_node, indent_level)
        lines.extend(left_lines)

        right_lines, right_var = parse_node(right_node, indent_level)
        lines.extend(right_lines)

        lines.append(
            f'{indent_str}{var_name} = set_equation("{op_}", {left_var}, {right_var})',
        )

    elif bname == BooleanType.INT_VALUE_COMPARISON:
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

    else:
        raise PanicError("Unsupported boolean")

    return lines, var_name


def handle_set_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "set" のノードを処理し、(コード行のリスト, 結果変数名) を返す。
    """
    lines: list[str] = []
    var_name = gen_var_name()
    indent_str = "    " * indent_level

    sname = node["name"]  # "B", "connect", etc.
    args = node.get("args", {})

    # 例に合わせた実装。必要に応じて拡張する。
    if sname == SetType.B:
        # 例えば {"struct": "P"} => board.b(Attribute.P)
        struct = args.get("struct")
        if struct == "P":
            lines.append(f"{indent_str}{var_name} = board.b(Attribute.P)")
        else:
            lines.append(f"{indent_str}# 未対応の struct: {struct}")
            lines.append(f"{indent_str}{var_name} = None")
    elif sname == SetType.CONNECT:
        # connect( variable, {Relationship.X, Relationship.Y, ...} )
        rels = args.get("relationship", [])
        child_var: str

        # variable が文字列ならそのまま、dict なら parse_node する
        variable_arg = args.get("variable")
        if isinstance(variable_arg, dict):
            # 再帰処理
            child_lines, child_var = parse_node(variable_arg, indent_level)
            lines.extend(child_lines)
        else:
            # 文字列(例: "dd")
            child_var = variable_arg

        # Relationship の集合を文字列化
        rel_set_str = "{" + ", ".join(f"Relationship.{r}" for r in rels) + "}"

        lines.append(f"{indent_str}{var_name} = connect({child_var}, {rel_set_str})")

    else:
        raise PanicError("Unsupported set type.")

    return lines, var_name


def handle_value_node(node: dict, indent_level: int = 1) -> tuple[list[str], str]:
    """
    "type": "value" ノードを処理し、(コード行リスト, 結果変数名) を返す。
    """
    lines: list[str] = []
    var_name = gen_var_name()
    indent_str = "    " * indent_level

    vname = node["name"]  # "int", "cross", など

    if vname == "int":
        # intの中に更に { "value": {...} } がある可能性
        sub_node = node["args"]["value"]
        sub_lines, sub_var = parse_node(sub_node, indent_level)
        lines.extend(sub_lines)
        # サンプル: int(...) みたいにラップするか、単に右辺をそのまま使うかは要件次第
        # ここでは便宜上、「そのまま代入する」ことにする
        lines.append(f"{indent_str}{var_name} = {sub_var}  # integer wrapper?")
    elif vname == "cross":
        # cross(dd)
        variable = node["args"]["variable"]
        lines.append(f"{indent_str}{var_name} = cross({variable})")
    else:
        lines.append(f"{indent_str}# Unsupported value node: {vname}")
        lines.append(f"{indent_str}{var_name} = None")

    return lines, var_name


def generate_code(json_data: dict) -> str:
    """
    汎用的に JSON データをパースし、最終的に main() 関数の中で
    トップレベルの式を生成して return する Python コードを返す。
    """
    constraints = json_data["constraints"]
    targets_list = []
    for constraint in constraints:
        targets_list.extend(constraint["targets"])
    targets = set(targets_list)
    # トップレベルのノードを parse
    top_lines, top_var = parse_node(json_data, 1)

    # コード組み立て
    lines = []
    lines.append("from __future__ import annotations")

    lines.append("import concurrent")
    lines.append("import tqdm")
    lines.append("from generator.checker.constants import *")
    lines.append("from generator.checker.dataclass import *")
    lines.append("from generator.checker.errors import *")
    lines.append("from generator.checker.function import *")
    lines.append("def solve(board: Board, targets: list[str]):")
    lines.append(f"{INDENT}board.shuffle(targets)")
    # 生成された行をインデント付きで入れる
    for ln in top_lines:
        lines.append(INDENT + ln)

    # 最後にトップレベルの結果を return するなど好きに処理
    # ここでは「return 変数」にしておく
    lines.append(f"{INDENT}return {top_var}")
    # fmt: off
    lines.append("def main():")
    lines.append(f"{INDENT}success = 0")
    lines.append(f"{INDENT}c_list = ElementList(HEIGHT, WIDTH, Attribute.C)")
    lines.append(f"{INDENT}p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)")
    lines.append(f"{INDENT}hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)")
    lines.append(f"{INDENT}vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)")
    lines.append(f"{INDENT}hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)")
    lines.append(f"{INDENT}vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)")
    lines.append(f"{INDENT}board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)")
    lines.append(f"{INDENT}targets = {targets.__str__()}")
    lines.append(f"{INDENT}with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:")
    lines.append(f"{INDENT}{INDENT}futures = [")
    lines.append(f"{INDENT}{INDENT}{INDENT}executor.submit(solve, board, targets) for _ in range(NUMBER_OF_SAMPLES)")
    lines.append(f"{INDENT}{INDENT}]")
    lines.append(f"{INDENT}{INDENT}with tqdm(total=len(futures)) as pbar:")
    lines.append(f"{INDENT}{INDENT}{INDENT}for future in concurrent.futures.as_completed(futures):")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}result = future.result()")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}success += 1")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}if CORRECT_RANGE[1] < success:")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}{INDENT}raise PanicError('成功回数が大きすぎました。')")
    lines.append(f"{INDENT}{INDENT}{INDENT}{INDENT}pbar.update(1)")
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
  "type": "boolean",
  "name": "quantifier",
  "properties": {
    "quantifier": "All",
    "variable": "dd",
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
                    "variable": {
                      "type": "set",
                      "name": "B",
                      "args": {
                        "struct": "P"
                      }
                    },
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
                        "variable": "dd"
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
"""
    data1 = json.loads(json_str1)
    code1 = generate_code(data1)
    print("=== Example 1: Top-level is quantifier ===")
    print(code1)
    print()

    # ------------------------------------------------------------
    # 例: トップレベルが quantifier じゃない場合 (単純に set_equation)
    # ------------------------------------------------------------
    json_str2 = r"""
{
  "type": "boolean",
  "name": "set_equation",
  "properties": {
    "op": "=="
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
      "name": "connect",
      "args": {
        "variable": "xx",
        "relationship": ["H","V"]
      }
    }
  }
}
"""
    data2 = json.loads(json_str2)
    code2 = generate_code(data2)
    print("=== Example 2: Top-level is set_equation ===")
    print(code2)

from __future__ import annotations

import subprocess


def run_poc():
    # 実行したいコマンドをリスト形式で指定
    cmd = [
        "poetry",
        "run",
        "python3",
        "puzzle_dsl_interpreter/generator/checker/poc.py",
    ]

    try:
        # stdout, stderr を取得したい場合は capture_output=True (3.7+)
        # または stdout=subprocess.PIPE, stderr=subprocess.PIPE を使う
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        # 実行結果
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)

        # returncode が 0 以外なら失敗とみなす（必要に応じてエラー処理）
        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            # 必要なら例外を投げたり、sys.exit() したりする

    except FileNotFoundError as e:
        # poetry がインストールされていない / PATH が通っていない場合など
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    run_poc()


if __name__ == "__main__":
    main()

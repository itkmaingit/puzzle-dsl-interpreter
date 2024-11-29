from __future__ import annotations

Primitive = int | str
Properties = dict[str, Primitive | "JSONObject" | "JSONArray"]
Elements = list[Primitive | "JSONObject"]


class Rule:
    def to_dict(self) -> dict:
        raise NotImplementedError("Subclasses must implement this method.")


# Object: キーが文字列、値が Primitive, JSONArray, または JSONObject の辞書
class JSONObject(Rule):
    def __init__(self, properties: Properties):
        self.properties = properties

    def __repr__(self):
        return f"JSONObject({self.properties})"


# Array: Primitive または Object を含むリスト
class JSONArray(Rule):
    def __init__(self, elements: Elements):
        self.elements = elements

    def __repr__(self):
        return f"JSONArray({self.elements})"

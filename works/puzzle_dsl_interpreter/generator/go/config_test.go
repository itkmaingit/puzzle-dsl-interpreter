package main

import (
	"reflect"
	"testing"
)

// TestFlatten は、Flatten 関数が元の多次元スライスの要素を正しくフラット化し、
// 要素の欠落や重複がないことを確認するテストです。
func TestFlatten(t *testing.T) {
	// 元の多次元スライスを初期化
	c, _, _, _, _, _ := InitializeElements()

	// Flatten 関数を適用
	newC := Flatten[*Element](c)

	// 元の多次元スライスの要素数をカウント
	originalCount := countElements(c)
	if originalCount != len(newC) {
		t.Errorf("要素数が一致しません。元の要素数: %d, フラット化後の要素数: %d", originalCount, len(newC))
	}

	// 元の要素をマップに収集
	originalElements := make(map[*Element]struct{})
	collectElements(c, originalElements)

	// フラット化された要素をマップに収集
	flattenedElements := make(map[*Element]struct{})
	for _, elem := range newC {
		flattenedElements[elem] = struct{}{}
	}

	// マップの要素数が一致するか確認
	if len(originalElements) != len(flattenedElements) {
		t.Errorf("ユニークな要素数が一致しません。元の要素数: %d, フラット化後の要素数: %d", len(originalElements), len(flattenedElements))
	}

	// 元の要素がフラット化後のスライスにすべて含まれているか確認
	for elem := range originalElements {
		if _, exists := flattenedElements[elem]; !exists {
			t.Errorf("元の要素 %v がフラット化後のスライスに存在しません。", elem)
		}
	}
}

// テストコード
func TestIsSubset(t *testing.T) {
	// テストケース 1: A は B の部分集合である
	A1 := [][][]int{
		{{1, 2}, {3}},
		{{4}},
	}
	B1 := [][][]int{
		{{1, 2, 3, 4, 5}},
		{{6, 7, 8}},
	}
	if !IsSubset[int](A1, B1) {
		t.Errorf("Test case 1 failed: A1 should be a subset of B1")
	}

	// テストケース 2: A は B の部分集合ではない
	A2 := [][][]int{
		{{1, 2}, {9}},
	}
	B2 := [][][]int{
		{{1, 2, 3, 4}},
	}
	if IsSubset[int](A2, B2) {
		t.Errorf("Test case 2 failed: A2 should not be a subset of B2")
	}

	// テストケース 3: A と B が同じ
	A3 := [][][]string{
		{{"a", "b"}, {"c"}},
	}
	B3 := [][][]string{
		{{"a", "b"}, {"c"}},
	}
	if !IsSubset[string](A3, B3) {
		t.Errorf("Test case 3 failed: A3 should be a subset of B3")
	}

	// テストケース 4: A が空
	A4 := [][][]int{}
	B4 := [][][]int{
		{{1, 2, 3}},
	}
	if !IsSubset[int](A4, B4) {
		t.Errorf("Test case 4 failed: Empty A4 should be a subset of B4")
	}

	// テストケース 5: B が空で A も空
	A5 := [][][]int{}
	B5 := [][][]int{}
	if !IsSubset[int](A5, B5) {
		t.Errorf("Test case 5 failed: Empty A5 should be a subset of empty B5")
	}

	// テストケース 6: B が空で A は空ではない
	A6 := [][][]int{
		{{1}},
	}
	B6 := [][][]int{}
	if IsSubset[int](A6, B6) {
		t.Errorf("Test case 6 failed: A6 should not be a subset of empty B6")
	}

	// テストケース 7: ポインタ型のテスト
	cList, _, _, _, _, _ := InitializeElements()
	p, _, _, _, _, _ := InitializeElements()
	if IsSubset[*Element](cList, p) {
		t.Errorf("Test case 7 failed: c should not be a subset of p")
	}

	// ポインタ型で部分集合ではない場合
	// p の要素を変更して c にない要素を持たせる
	// ここではシミュレーションのため、p の最初の要素を新しい *Element に置き換えます
	p[0][0] = &Element{Value: 999, Attr: C, N: 0, M: 0}
	if IsSubset[*Element](cList, p) {
		t.Errorf("Test case 8 failed: c should not be a subset of modified p")
	}

	// --- テストケース 9: cList のコピーを作成して部分集合であることを確認 ---
	// cList のコピーを作成
	cListCopy := make([][]*Element, len(cList))
	for i := range cList {
		cListCopy[i] = make([]*Element, len(cList[i]))
		copy(cListCopy[i], cList[i])
	}

	// cListCopy が cList の部分集合であることを確認
	if !IsSubset[*Element](cListCopy, cList) {
		t.Errorf("Test case 9 failed: cListCopy should be a subset of cList")
	}

	// cListCopy の要素を変更して部分集合ではなくなるようにする
	cListCopy[0][0] = &Element{Value: -2, Attr: C, N: 0, M: 0}

	// cListCopy が cList の部分集合ではないことを確認
	if IsSubset[*Element](cListCopy, cList) {
		t.Errorf("Test case 10 failed: modified cListCopy should not be a subset of cList")
	}
}

func TestIsIn(t *testing.T) {
	// テストケース 1: A が B に直接含まれている
	A1 := 5
	B1 := []interface{}{1, 2, 3, 4, 5}
	if !IsIn[int](A1, B1) {
		t.Errorf("Test case 1 failed: %v should be in %v", A1, B1)
	}

	// テストケース 2: A が B のネストされたスライスに含まれている
	A2 := []int{1, 2}
	B2 := []interface{}{0, []int{1, 2}, 3}
	if !IsIn[[]int](A2, B2) {
		t.Errorf("Test case 2 failed: %v should be in %v", A2, B2)
	}

	// テストケース 3: A が B に含まれていない
	A3 := "not_in_slice"
	B3 := []interface{}{"a", "b", "c"}
	if IsIn[string](A3, B3) {
		t.Errorf("Test case 3 failed: %v should not be in %v", A3, B3)
	}

	// テストケース 4: A がネストされた深い階層に含まれている
	A4 := 42
	B4 := []interface{}{
		1,
		[]interface{}{
			2,
			[]interface{}{
				3, 42,
			},
		},
	}
	if !IsIn[int](A4, B4) {
		t.Errorf("Test case 4 failed: %v should be in %v", A4, B4)
	}

	// テストケース 5: A が B の多次元スライスの要素として含まれている
	A5 := [][]int{{1, 2}, {3, 4}}
	B5 := []interface{}{
		5,
		[][]int{{1, 2}, {3, 4}},
		7,
	}
	if !IsIn[[][]int](A5, B5) {
		t.Errorf("Test case 5 failed: %v should be in %v", A5, B5)
	}

	// テストケース 6: A と B が同じ値だが異なるインスタンス
	A6 := &Element{Value: 10, Attr: C, N: 0, M: 0}
	B6 := []interface{}{
		&Element{Value: 10, Attr: C, N: 0, M: 0},
	}
	if !IsIn[*Element](A6, B6) {
		t.Errorf("Test case 6 failed: %v should be in %v", A6, B6)
	}

	// テストケース 7: InitializeElements() から生成されたデータを使用
	cList, _, _, _, _, _ := InitializeElements()
	A7 := cList[0][0] // cList の最初の要素
	B7 := cList       // cList 全体
	if !IsIn[*Element](A7, B7) {
		t.Errorf("Test case 7 failed: A7 should be in B7")
	}

	// テストケース 8: A が B に含まれていない場合（InitializeElements を使用）
	A8 := &Element{Value: -1, Attr: C, N: -1, M: -1}
	B8 := cList
	if IsIn[*Element](A8, B8) {
		t.Errorf("Test case 8 failed: A8 should not be in B8")
	}

	// テストケース 9: A が B のネストされたスライスの中に含まれている（ポインタ型）
	A9 := cList[1]
	B9 := cList
	if !IsIn[[]*Element](A9, B9) {
		t.Errorf("Test case 9 failed: A9 should be in B9")
	}

	// テストケース 10: A がスライスで、B の要素と一致しない
	A10 := []*Element{
		{Value: -2, Attr: C, N: 0, M: 0},
	}
	B10 := cList
	if IsIn[[]*Element](A10, B10) {
		t.Errorf("Test case 10 failed: A10 should not be in B10")
	}
}

// テストコード
func TestAllDifferent(t *testing.T) {
	// テストケース 1: すべての要素の Value が異なる場合
	elements1 := []*Element{
		{Value: 1, Attr: "Attr1", N: 0, M: 0},
		{Value: 2, Attr: "Attr2", N: 0, M: 1},
		{Value: 3, Attr: "Attr3", N: 1, M: 0},
		{Value: 4, Attr: "Attr4", N: 1, M: 1},
	}
	if !AllDifferent(elements1) {
		t.Errorf("Test case 1 failed: expected true, got false")
	}

	// テストケース 2: Value に重複がある場合
	elements2 := []*Element{
		{Value: 1, Attr: "Attr1", N: 0, M: 0},
		{Value: 2, Attr: "Attr2", N: 0, M: 1},
		{Value: 1, Attr: "Attr3", N: 1, M: 0}, // Value が重複
		{Value: 4, Attr: "Attr4", N: 1, M: 1},
	}
	if AllDifferent(elements2) {
		t.Errorf("Test case 2 failed: expected false, got true")
	}

	// テストケース 3: 空のスライス
	elements3 := []*Element{}
	if !AllDifferent(elements3) {
		t.Errorf("Test case 3 failed: expected true for empty slice, got false")
	}

	// テストケース 4: 要素が一つだけの場合
	elements4 := []*Element{
		{Value: 42, Attr: "Attr42", N: 0, M: 0},
	}
	if !AllDifferent(elements4) {
		t.Errorf("Test case 4 failed: expected true for single element, got false")
	}

	// テストケース 5: Value がすべて同じ場合
	elements5 := []*Element{
		{Value: 5, Attr: "Attr5", N: 0, M: 0},
		{Value: 5, Attr: "Attr5", N: 0, M: 1},
		{Value: 5, Attr: "Attr5", N: 1, M: 0},
	}
	if AllDifferent(elements5) {
		t.Errorf("Test case 5 failed: expected false, got true")
	}

	// テストケース 6: InitializeElements() から生成されたデータを使用
	cList, _, _, _, _, _ := InitializeElements()
	flattenedCList := Flatten[*Element](cList)

	// 重複がない場合を確認
	if AllDifferent(flattenedCList) {
		t.Errorf("Test case 6 failed: expected true, got false")
	}

	// Value を重複させる
	if len(flattenedCList) >= 2 {
		flattenedCList[1].Value = flattenedCList[0].Value
		if AllDifferent(flattenedCList) {
			t.Errorf("Test case 7 failed: expected false after introducing duplicate, got true")
		}
	}
}

// countElements は、多次元スライス内の *Element 型の要素数を再帰的にカウントします。
func countElements(input interface{}) int {
	count := 0
	v := reflect.ValueOf(input)
	switch v.Kind() {
	case reflect.Slice:
		for i := 0; i < v.Len(); i++ {
			count += countElements(v.Index(i).Interface())
		}
	case reflect.Ptr:
		if _, ok := input.(*Element); ok {
			count = 1
		}
	}
	return count
}

// collectElements は、多次元スライス内の *Element 型の要素をマップに収集します。
func collectElements(input interface{}, elements map[*Element]struct{}) {
	v := reflect.ValueOf(input)
	switch v.Kind() {
	case reflect.Slice:
		for i := 0; i < v.Len(); i++ {
			collectElements(v.Index(i).Interface(), elements)
		}
	case reflect.Ptr:
		if elem, ok := input.(*Element); ok {
			elements[elem] = struct{}{}
		}
	}
}

package main

import (
	"math/rand"
	"testing"
)

const (
	testHeight = 3
	testWidth  = 3
)

// TestFlatten は、flattenSlice 関数が元の多次元スライスの要素を正しくフラット化し、
// 要素の欠落や重複がないことを確認するテストです。
func TestFlatten(t *testing.T) {
	// 固定乱数生成器の初期化 (テストの再現性を確保)
	randGen := rand.New(rand.NewSource(42))

	// 元の多次元スライスを初期化
	cList, _, _, _, _, _ := InitializeElements(randGen)

	originalCount := AbsoluteSet(cList)
	// flattenSlice 関数を適用
	flattened := flattenSlice[*Element](cList)

	// 元の多次元スライスの要素数をカウント
	if originalCount != len(flattened) {
		t.Errorf("要素数が一致しません。元の要素数: %d, フラット化後の要素数: %d", originalCount, len(flattened))
	}

	// 元の要素をマップに収集
	originalElements := make(map[*Element]struct{})
	collectElements(cList, originalElements)

	// フラット化された要素をマップに収集
	flattenedElements := make(map[*Element]struct{})
	for _, elem := range flattened {
		flattenedElements[elem] = struct{}{}
	}

	// マップの要素数が一致するか確認
	if len(originalElements) != len(flattenedElements) {
		t.Errorf("ユニークな要素数が一致しません。元の要素数: %d, フラット化後の要素数: %d", len(originalElements), len(flattenedElements))
	}

	// 元の要素がフラット化後のスライスにすべて含まれているか確認
	for elem := range originalElements {
		if _, exists := flattenedElements[elem]; !exists {
			t.Errorf("元の要素 %+v がフラット化後のスライスに存在しません。", elem)
		}
	}
}

// collectElements は、多次元スライス内の *Element 型の要素をマップに収集します。
func collectElements(input interface{}, elements map[*Element]struct{}) {
	switch v := input.(type) {
	case []*Element:
		for _, elem := range v {
			if elem != nil {
				elements[elem] = struct{}{}
			}
		}
	case [][]*Element:
		for _, row := range v {
			collectElements(row, elements)
		}
	case [][][]*Element:
		for _, matrix := range v {
			collectElements(matrix, elements)
		}
		// 必要に応じてさらに多次元に対応
	}
}

// TestIsSubset は、IsSubset 関数の動作を検証するテストです。
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
	cList, pList, _, _, _, _ := initTestElements()
	if IsSubset[*Element](cList, pList) {
		t.Errorf("Test case 7 failed: cList should not be a subset of pList")
	}

	// ポインタ型で部分集合ではない場合
	// p の最初の要素を新しい *Element に置き換える
	if len(pList) > 0 && len(pList[0]) > 0 {
		pList[0][0] = &Element{Value: 999, Attr: C, N: 0, M: 0}
		if IsSubset[*Element](cList, pList) {
			t.Errorf("Test case 8 failed: cList should not be a subset of modified pList")
		}
	}

	// テストケース 9: cList のコピーを作成して部分集合であることを確認
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
	if len(cListCopy) > 0 && len(cListCopy[0]) > 0 {
		cListCopy[0][0] = &Element{Value: -2, Attr: C, N: 0, M: 0}
		if IsSubset[*Element](cListCopy, cList) {
			t.Errorf("Test case 10 failed: modified cListCopy should not be a subset of cList")
		}
	}
}

// TestAllDifferent は、AllDifferent 関数の動作を検証するテストです。
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
	cList, _, _, _, _, _ := initTestElements()
	flattenedCList := flattenSlice[*Element](cList)

	// AllDifferent の結果が期待通りか確認
	// InitializeElements で乱数を使っているため、結果はシードに依存します
	// この例では、シードを固定しているため結果も固定
	expectedAllDifferent := true
	seenValues := make(map[int]struct{})
	for _, elem := range flattenedCList {
		if _, exists := seenValues[elem.Value]; exists {
			expectedAllDifferent = false
			break
		}
		seenValues[elem.Value] = struct{}{}
	}
	if AllDifferent(flattenedCList) != expectedAllDifferent {
		t.Errorf("Test case 6 failed: AllDifferent(flattenedCList) = %v; expected %v", AllDifferent(flattenedCList), expectedAllDifferent)
	}

	// Value を重複させる
	if len(flattenedCList) >= 2 {
		flattenedCList[1].Value = flattenedCList[0].Value
		if AllDifferent(flattenedCList) {
			t.Errorf("Test case 7 failed: expected false after introducing duplicate, got true")
		}
	}
}

// TestIsHorizontal は、isHorizontal 関数の動作を検証するテストです。
func TestIsHorizontal(t *testing.T) {
	// 例: c(0,0) と c(0,1) は同じ行で列が±1なので Horizontal のはず
	e1 := &Element{N: 0, M: 0, Attr: C}
	e2 := &Element{N: 0, M: 1, Attr: C}
	if !isHorizontal(e1, e2) {
		t.Errorf("expected isHorizontal(e1,e2) = true, got false")
	}

	// 縦方向に並んでいるものは false になるはず
	e3 := &Element{N: 1, M: 0, Attr: C}
	if isHorizontal(e1, e3) {
		t.Errorf("expected isHorizontal(e1,e3) = false, got true")
	}

	// p(0,0) & p(0,1) => true
	e4 := &Element{N: 0, M: 0, Attr: P}
	e5 := &Element{N: 0, M: 1, Attr: P}
	if !isHorizontal(e4, e5) {
		t.Errorf("expected isHorizontal(e4,e5) = true, got false")
	}

	// p(0,0) & p(1,0) => false
	e6 := &Element{N: 1, M: 0, Attr: P}
	if isHorizontal(e4, e6) {
		t.Errorf("expected isHorizontal(e4,e6) = false, got true")
	}

	// Hp と Hc が同じ属性の場合
	e7 := &Element{N: 0, M: 0, Attr: Hp}
	e8 := &Element{N: 0, M: 1, Attr: Hp}
	if !isHorizontal(e7, e8) {
		t.Errorf("expected isHorizontal(e7,e8) = true, got false")
	}

	// 異なる属性間の横隣接
	e9 := &Element{N: 0, M: 0, Attr: C}
	e10 := &Element{N: 0, M: 1, Attr: P}
	if isHorizontal(e9, e10) {
		t.Errorf("expected isHorizontal(e9,e10) = false, got true")
	}
}

// TestIsVertical は、isVertical 関数の動作を検証するテストです。
func TestIsVertical(t *testing.T) {
	// p(0,0) と p(1,0) は同じ列で行が±1なので Vertical のはず
	e1 := &Element{N: 0, M: 0, Attr: P}
	e2 := &Element{N: 1, M: 0, Attr: P}
	if !isVertical(e1, e2) {
		t.Errorf("expected isVertical(e1,e2) = true, got false")
	}

	// 横方向に並んでいるものは false になるはず
	e3 := &Element{N: 0, M: 1, Attr: P}
	if isVertical(e1, e3) {
		t.Errorf("expected isVertical(e1,e3) = false, got true")
	}

	// c(0,0) と c(1,0) => true
	e4 := &Element{N: 0, M: 0, Attr: C}
	e5 := &Element{N: 1, M: 0, Attr: C}
	if !isVertical(e4, e5) {
		t.Errorf("expected isVertical(e4,e5) = true, got false")
	}

	// c(0,0) と c(0,1) => false
	e6 := &Element{N: 0, M: 1, Attr: C}
	if isVertical(e4, e6) {
		t.Errorf("expected isVertical(e4,e6) = false, got true")
	}

	// Vp と Vc が同じ属性の場合
	e7 := &Element{N: 0, M: 0, Attr: Vp}
	e8 := &Element{N: 1, M: 0, Attr: Vp}
	if !isVertical(e7, e8) {
		t.Errorf("expected isVertical(e7,e8) = true, got false")
	}

	// 異なる属性間の縦隣接
	e9 := &Element{N: 0, M: 0, Attr: C}
	e10 := &Element{N: 1, M: 0, Attr: P}
	if isVertical(e9, e10) {
		t.Errorf("expected isVertical(e9,e10) = false, got true")
	}
}

// TestIsDiagonal は、isDiagonal 関数の動作を検証するテストです。
func TestIsDiagonal(t *testing.T) {
	// c(0,0), c(1,1) => 斜め (|0-1|=1, |0-1|=1) => true
	e1 := &Element{N: 0, M: 0, Attr: C}
	e2 := &Element{N: 1, M: 1, Attr: C}
	if !isDiagonal(e1, e2) {
		t.Errorf("expected isDiagonal(e1,e2) = true, got false")
	}

	// まったく斜めでないもの => false
	e3 := &Element{N: 1, M: 0, Attr: C}
	if isDiagonal(e1, e3) {
		t.Errorf("expected isDiagonal(e1,e3) = false, got true")
	}

	// p(0,0) と p(1,1) => 斜め
	e4 := &Element{N: 0, M: 0, Attr: P}
	e5 := &Element{N: 1, M: 1, Attr: P}
	if !isDiagonal(e4, e5) {
		t.Errorf("expected isDiagonal(e4,e5) = true, got false")
	}

	// p(0,0) と p(1,0) => 斜めではない
	e6 := &Element{N: 1, M: 0, Attr: P}
	if isDiagonal(e4, e6) {
		t.Errorf("expected isDiagonal(e4,e6) = false, got true")
	}

	// Hp と Vp の斜隣接
	e7 := &Element{N: 2, M: 2, Attr: Hp}
	e8 := &Element{N: 1, M: 2, Attr: Vp} // dI = -1, dJ = 1
	if !isDiagonal(e7, e8) {
		t.Errorf("expected isDiagonal(e7,e8) = true, got false")
	}

	// Vp と Hp の斜隣接
	e9 := &Element{N: 2, M: 2, Attr: Hp}
	e10 := &Element{N: 2, M: 3, Attr: Vp}
	if !isDiagonal(e10, e9) {
		t.Errorf("expected isDiagonal(e10,e9) = true, got false")
	}

	// Hc と Vc の斜隣接
	e11 := &Element{N: 2, M: 2, Attr: Hc}
	e12 := &Element{N: 1, M: 2, Attr: Vc}
	if !isDiagonal(e11, e12) {
		t.Errorf("expected isDiagonal(e11,e12) = true, got false")
	}

	// Vc と Hc の斜隣接
	e13 := &Element{N: 3, M: 2, Attr: Hc}
	e14 := &Element{N: 2, M: 2, Attr: Vc}
	if !isDiagonal(e14, e13) {
		t.Errorf("expected isDiagonal(e14,e13) = true, got false")
	}
}

// TestConnect は、Connect 関数の動作を検証するテストです。
func TestConnect(t *testing.T) {
	// テスト用の小さな ElementList を作成
	cList, _, _, _, _, _ := initTestElements()

	// ここでは cList[0][0] を中心に、H, V, D, M をひととおり拾ってみるテスト
	center := cList[0][0] // 例: c(0,0)

	// H, V, D, M 全部取ってみる
	neighbors := Connect(center, []Relationship{H, V, D, Relationship("M")}, cList)

	// cList は 2x2 なので Flatten して要素は4つ: c(0,0), c(0,1), c(1,0), c(1,1)
	// うち、center 本人以外の 3 つのうち “横/縦/斜め/一致” を満たすものがあれば neighbors に入る
	// → 例えば “横隣 = c(0,1)”, “縦隣 = c(1,0)”, “斜隣 = c(1,1)”

	// 期待される neighbors の数は 3 (c(0,1), c(1,0), c(1,1))
	expectedNeighborsCount := 3
	if len(neighbors) != expectedNeighborsCount {
		t.Errorf("expected %d neighbors for c(0,0), got %d. neighbors: %v", expectedNeighborsCount, len(neighbors), neighbors)
	}

	// 期待される neighbors の内容を確認
	expectedNeighbors := []*Element{
		cList[0][1], // H
		cList[1][0], // V
		cList[1][1], // D
	}

	for _, expected := range expectedNeighbors {
		found := false
		for _, neighbor := range neighbors {
			if neighbor.Equal(expected) {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("expected neighbor %+v not found in neighbors: %v", expected, neighbors)
		}
	}

	// 例えば “横だけ” を拾う場合は
	hNeighbors := Connect(center, []Relationship{H}, cList)
	// c(0,0) から見た “横” は c(0,1) だけのはず
	expectedHNeighbors := []*Element{
		cList[0][1],
	}

	if len(hNeighbors) != len(expectedHNeighbors) {
		t.Errorf("expected %d horizontal neighbors for c(0,0), got %d. hNeighbors: %v", len(expectedHNeighbors), len(hNeighbors), hNeighbors)
	}

	for _, expected := range expectedHNeighbors {
		found := false
		for _, neighbor := range hNeighbors {
			if neighbor.Equal(expected) {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("expected horizontal neighbor %+v not found in hNeighbors: %v", expected, hNeighbors)
		}
	}

	// “M” 関係性は未定義なので、追加のテストを行いますが、現在の isRelated 関数では "M" は false となります
	mNeighbors := Connect(center, []Relationship{Relationship("M")}, cList)
	if len(mNeighbors) != 0 {
		t.Errorf("expected 0 'M' neighbors for c(0,0), got %d. mNeighbors: %v", len(mNeighbors), mNeighbors)
	}
}

// initTestElements は、テスト用の小さな ElementList を作成します。
func initTestElements() (ElementList, ElementList, ElementList, ElementList, ElementList, ElementList) {
	// 固定乱数生成器の初期化 (テストの再現性を確保)
	randGen := rand.New(rand.NewSource(42))

	// candidates を小さめに
	pointCandidates := []int{0, 1}
	edgeCandidates := []int{0, 1}

	cList := NewElementList(randGen, testHeight, testWidth, pointCandidates, C)
	pList := NewElementList(randGen, testHeight+1, testWidth+1, pointCandidates, P)
	hcList := NewElementList(randGen, testHeight, testWidth-1, edgeCandidates, Hc)
	vcList := NewElementList(randGen, testHeight-1, testWidth, edgeCandidates, Vc)
	hpList := NewElementList(randGen, testHeight+1, testWidth, edgeCandidates, Hp)
	vpList := NewElementList(randGen, testHeight, testWidth+1, edgeCandidates, Vp)
	return cList, pList, hcList, vcList, hpList, vpList
}

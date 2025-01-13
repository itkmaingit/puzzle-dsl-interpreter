package main

import (
	"fmt"
	"log"
	"math"
	"math/rand"
	"reflect"
	"time"

	"github.com/google/go-cmp/cmp"
)

// Attribute および Relationship の定義
type Attribute string
type Relationship string

// 定数の定義
const (
	C  = Attribute("C")
	P  = Attribute("P")
	Hp = Attribute("Hp")
	Vp = Attribute("Vp")
	Hc = Attribute("Hc")
	Vc = Attribute("Vc")

	H = Relationship("H")
	V = Relationship("V")
	D = Relationship("D")

	HEIGHT = 4
	WIDTH  = 4
)

// Element 構造体の定義
type Element struct {
	Value int
	Attr  Attribute
	N     int // 行番号
	M     int // 列番号
}

// Equal メソッド: フィールドがすべて一致しているかを比較
func (e *Element) Equal(other *Element) bool {
	if e == nil || other == nil {
		return false
	}
	return e.Value == other.Value && e.Attr == other.Attr && e.N == other.N && e.M == other.M
}

// ElementList の定義
type ElementList [][]*Element

// Board 構造体: すべての ElementList を管理し、効率的なアクセスを提供
type Board struct {
	cList  ElementList
	pList  ElementList
	hcList ElementList
	vcList ElementList
	hpList ElementList
	vpList ElementList

	elementsMap map[[3]int]*Element // [Attribute, N, M] -> *Element
	randGen     *rand.Rand          // 乱数生成器
}

// NewElement 関数: 指定された候補からランダムに選んで Element を作成
func NewElement(r *rand.Rand, candidates []int, attr Attribute, n int, m int) *Element {
	if len(candidates) == 0 {
		log.Panic("candidates slice cannot be empty")
	}
	randIdx := r.Intn(len(candidates))
	value := candidates[randIdx]
	return &Element{Value: value, Attr: attr, N: n, M: m}
}

// NewElementList 関数: 指定された高さ・幅・候補から ElementList を作成
func NewElementList(r *rand.Rand, height int, width int, candidates []int, attr Attribute) ElementList {
	ret := make(ElementList, height)
	for i := 0; i < height; i++ {
		ret[i] = make([]*Element, width)
		for j := 0; j < width; j++ {
			ret[i][j] = NewElement(r, candidates, attr, i, j)
		}
	}
	return ret
}

// InitializeElements 関数: 各種 ElementList を初期化
func InitializeElements(r *rand.Rand) (ElementList, ElementList, ElementList, ElementList, ElementList, ElementList) {
	pointCandidates := []int{0, 1, 2, 3, 4}
	edgeCandidates := []int{0, 1}
	cList := NewElementList(r, HEIGHT, WIDTH, pointCandidates, C)
	pList := NewElementList(r, HEIGHT+1, WIDTH+1, pointCandidates, P)
	hcList := NewElementList(r, HEIGHT, WIDTH-1, edgeCandidates, Hc)
	vcList := NewElementList(r, HEIGHT-1, WIDTH, edgeCandidates, Vc)
	hpList := NewElementList(r, HEIGHT+1, WIDTH, edgeCandidates, Hp)
	vpList := NewElementList(r, HEIGHT, WIDTH+1, edgeCandidates, Vp)
	return cList, pList, hcList, vcList, hpList, vpList
}

// NewBoard 関数: 既存の ElementList を受け取り、Board を初期化
func NewBoard(cList, pList, hcList, vcList, hpList, vpList ElementList) *Board {
	board := &Board{
		cList:       cList,
		pList:       pList,
		hcList:      hcList,
		vcList:      vcList,
		hpList:      hpList,
		vpList:      vpList,
		elementsMap: make(map[[3]int]*Element),
		randGen:     rand.New(rand.NewSource(time.Now().UnixNano())),
	}

	// マップにすべての要素を登録
	board.registerElements(C, board.cList)
	board.registerElements(P, board.pList)
	board.registerElements(Hc, board.hcList)
	board.registerElements(Vc, board.vcList)
	board.registerElements(Hp, board.hpList)
	board.registerElements(Vp, board.vpList)

	return board
}

// registerElements は指定された Attribute と ElementList をマップに登録します
func (b *Board) registerElements(attr Attribute, elist ElementList) {
	for i, row := range elist {
		for j, elem := range row {
			if elem != nil && elem.Attr == attr && elem.N == i && elem.M == j {
				key := [3]int{int(elem.Attr[0]), elem.N, elem.M}
				b.elementsMap[key] = elem
			}
		}
	}
}

// getElement メソッド: 指定された Attribute と座標 (i, j) に基づいて Element を取得
func (b *Board) getElement(attr Attribute, i, j int) *Element {
	key := [3]int{int(attr[0]), i, j}
	return b.elementsMap[key]
}

// isRelated は、Relationship に基づいて要素間の関係を判定します
func isRelated(e, o *Element, r Relationship) bool {
	switch r {
	case H:
		return isHorizontal(e, o)
	case V:
		return isVertical(e, o)
	case D:
		return isDiagonal(e, o)
	default:
		// 未知の Relationship は無効とする
		return false
	}
}

// isHorizontal は、論文で定義される「横隣接」を判定します
func isHorizontal(e, o *Element) bool {
	i, j := e.N, e.M
	i2, j2 := o.N, o.M
	a, a2 := e.Attr, o.Attr

	// 同じ行かつ列差が1で、かつ属性が一致する場合
	if i == i2 && int(math.Abs(float64(j-j2))) == 1 {
		switch a {
		case P, C, Hp, Hc:
			if a == a2 {
				return true
			}
		}
	}
	return false
}

// isVertical は、論文で定義される「縦隣接」を判定します
func isVertical(e, o *Element) bool {
	i, j := e.N, e.M
	i2, j2 := o.N, o.M
	a, a2 := e.Attr, o.Attr

	// 同じ列かつ行差が1で、かつ属性が一致する場合
	if j == j2 && int(math.Abs(float64(i-i2))) == 1 {
		switch a {
		case P, C, Vp, Vc:
			if a == a2 {
				return true
			}
		}
	}
	return false
}

// isDiagonal は、論文で定義される「斜隣接」を判定します
func isDiagonal(e, o *Element) bool {
	i, j := e.N, e.M
	i2, j2 := o.N, o.M
	a, a2 := e.Attr, o.Attr

	// 行差と列差が1で、かつ属性が一致する場合
	if int(math.Abs(float64(i-i2))) == 1 && int(math.Abs(float64(j-j2))) == 1 {
		switch a {
		case P, C:
			if a == a2 {
				return true
			}
		}
	}

	// 特定の属性間の斜隣接
	// 例: Hp と Vp の場合
	if a == Hp && a2 == Vp {
		dI := i - i2
		dJ := j - j2
		if (dI == 0 || dI == 1) && (dJ == 0 || dJ == -1) {
			return true
		}
	}
	if a == Vp && a2 == Hp {
		dI := i - i2
		dJ := j - j2
		if (dI == 0 || dI == -1) && (dJ == 0 || dJ == 1) {
			return true
		}
	}

	// 例: Hc と Vc の場合
	if a == Hc && a2 == Vc {
		dI := i - i2
		dJ := j - j2
		if (dI == 0 || dI == 1) && (dJ == 0 || dJ == -1) {
			return true
		}
	}
	if a == Vc && a2 == Hc {
		dI := i - i2
		dJ := j - j2
		if (dI == 0 || dI == -1) && (dJ == 0 || dJ == 1) {
			return true
		}
	}

	return false
}

// Connect 関数:
//
//	e        : 中心となる *Element
//	rels     : 判定したい隣接関係の種類 (H, V, D) が並んだスライス
//	grid     : 探索対象となる ElementList (多次元)
func Connect(e *Element, rels []Relationship, grid ElementList) []*Element {
	var result []*Element

	// grid の全要素をフラット化
	flattened := flattenElements(grid)

	for _, other := range flattened {
		// 同一要素なら無視
		if e.Equal(other) {
			continue
		}
		// rels に含まれるどれか1つでも関係を満たせば追加
		for _, r := range rels {
			if isRelated(e, other, r) {
				result = append(result, other)
				break
			}
		}
	}
	return result
}

// flattenElements は ElementList をフラットなスライスに変換します
func flattenElements(grid ElementList) []*Element {
	var flattened []*Element
	for _, row := range grid {
		for _, elem := range row {
			if elem != nil {
				flattened = append(flattened, elem)
			}
		}
	}
	return flattened
}

// Solution は Element の Value を返すシンプルな関数です。
// 実際の用途に応じて適切に実装してください。
func Solution(e *Element) int {
	return e.Value
}

// AbsoluteSet は、多次元スライス内の *Element 型の要素数を再帰的にカウントします。
func AbsoluteSet(input interface{}) int {
	count := 0
	switch v := input.(type) {
	case []*Element:
		for _, elem := range v {
			if elem != nil {
				count++
			}
		}
	case [][]*Element:
		for _, row := range v {
			count += AbsoluteSet(row)
		}
	case ElementList:
		for _, row := range v {
			count += AbsoluteSet(row)
		}
	case [][][]*Element:
		for _, matrix := range v {
			count += AbsoluteSet(matrix)
		}
	default:
		// その他の型はカウントしない
	}
	return count
}

// IsSubset は、任意の型 T の多次元スライス A と B を受け取り、A の要素がすべて B に含まれているかを判定します。
func IsSubset[T any](A any, B any) bool {
	flattenedA := flattenSlice[T](A)
	flattenedB := flattenSlice[T](B)

	// A の各要素が B に存在するかをチェック
	for _, aElem := range flattenedA {
		found := false
		for _, bElem := range flattenedB {
			if cmp.Equal(aElem, bElem) {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}
	return true
}

// IsIn は、任意の型 T の多次元スライス B と値 A を受け取り、
// A が B の要素として含まれているかどうかを判定します。
func IsIn[T comparable](A T, B any) bool {
	flattenedB := flattenSlice[T](B)
	for _, elem := range flattenedB {
		if elem == A {
			return true
		}
	}
	return false
}

// AllDifferent は、与えられた []*Element スライス内の各要素の Value フィールドがすべて異なる場合に true を返します。
func AllDifferent(elements []*Element) bool {
	valueSet := make(map[int]struct{})
	for _, elem := range elements {
		if _, exists := valueSet[elem.Value]; exists {
			return false
		}
		valueSet[elem.Value] = struct{}{}
	}
	return true
}

// Flatten は多次元スライス input を受け取り、一次元のスライス []T に平坦化します。
func flattenSlice[T any](input any) []T {
	var result []T
	flattenRecursive[T](input, &result)
	return result
}

// flattenRecursive は再帰的に多次元スライスを走査し、要素を result に追加します。
func flattenRecursive[T any](input any, result *[]T) {
	v := reflect.ValueOf(input)

	switch v.Kind() {
	case reflect.Slice, reflect.Array:
		for i := 0; i < v.Len(); i++ {
			flattenRecursive[T](v.Index(i).Interface(), result)
		}
	default:
		// 型アサーションを行い、型が一致する場合に result に追加
		if value, ok := input.(T); ok {
			*result = append(*result, value)
		} else {
			// 型が一致しない場合はエラーを出力（必要に応じてエラーハンドリングを追加）
			fmt.Printf("型が一致しません: %v\n", input)
		}
	}
}

// cross 関数:
//
//	e    : 中心となる *Element
//	board: 要素が配置された Board
//
// 戻り値: 関連する Hp と Vp の Value の合計
func cross(e *Element, board *Board) (int, error) {
	if e.Attr != P {
		return 0, fmt.Errorf("element at (%d,%d) is not P", e.N, e.M)
	}
	i, j := e.N, e.M
	sum := 0

	// Hp 要素を取得: (i, j-1) と (i, j)
	hp1 := board.getElement(Hp, i, j-1)
	if hp1 != nil {
		sum += hp1.Value
	}
	hp2 := board.getElement(Hp, i, j)
	if hp2 != nil {
		sum += hp2.Value
	}

	// Vp 要素を取得: (i-1, j) と (i-1, j+1)
	vp1 := board.getElement(Vp, i-1, j)
	if vp1 != nil {
		sum += vp1.Value
	}
	vp2 := board.getElement(Vp, i-1, j+1)
	if vp2 != nil {
		sum += vp2.Value
	}

	return sum, nil
}

// cycle 関数:
//
//	board: 要素が配置された Board
//
// 戻り値: 各 P 要素の座標とその cross の合計値のマップ
func cycle(board *Board) map[[2]int]int {
	results := make(map[[2]int]int)

	for i := 0; i < len(board.pList); i++ {
		for j := 0; j < len(board.pList[i]); j++ {
			pElement := board.pList[i][j]
			if pElement != nil && pElement.Attr == P {
				sum, err := cross(pElement, board)
				if err != nil {
					// P でない要素は無視
					continue
				}
				results[[2]int{i, j}] = sum
			}
		}
	}

	return results
}

// main 関数: サンプル実行
func main() {
	// 乱数生成器の初期化
	randGen := rand.New(rand.NewSource(42))

	// ElementList の初期化
	cList, pList, _, _, _, _ := InitializeElements(randGen)
	if IsSubset[*Element](cList, pList) {
		fmt.Printf("Why!!!")
		// t.Errorf("Test case 7 failed: cList should not be a subset of pList")
	}
	// // Board の初期化
	// board := NewBoard(cList, pList, hcList, vcList, hpList, vpList)

	// // 特定の要素の Value と Attribute を設定
	// // p(2,2)
	// p22 := board.getElement(P, 2, 2)
	// if p22 != nil {
	// 	p22.Value = 10
	// }

	// hp21 := board.getElement(Hp, 2, 1)
	// if hp21 != nil {
	// 	hp21.Value = 5
	// }
	// hp22 := board.getElement(Hp, 2, 2)
	// if hp22 != nil {
	// 	hp22.Value = 7
	// }

	// vp12 := board.getElement(Vp, 1, 2)
	// if vp12 != nil {
	// 	vp12.Value = 3
	// }
	// vp13 := board.getElement(Vp, 1, 3)
	// if vp13 != nil {
	// 	vp13.Value = 4
	// }

	// // p(1,1) の場合
	// p11 := board.getElement(P, 1, 1)
	// if p11 != nil {
	// 	p11.Value = 20
	// }

	// hp10 := board.getElement(Hp, 1, 0)
	// if hp10 != nil {
	// 	hp10.Value = 6
	// }
	// hp11 := board.getElement(Hp, 1, 1)
	// if hp11 != nil {
	// 	hp11.Value = 8
	// }

	// vp01 := board.getElement(Vp, 0, 1)
	// if vp01 != nil {
	// 	vp01.Value = 2
	// }
	// vp02 := board.getElement(Vp, 0, 2)
	// if vp02 != nil {
	// 	vp02.Value = 1
	// }

	// // p(0,0) の場合
	// p00 := board.getElement(P, 0, 0)
	// if p00 != nil {
	// 	p00.Value = 15
	// }

	// hp00 := board.getElement(Hp, 0, 0)
	// if hp00 != nil {
	// 	hp00.Value = 2
	// }

	// // cross 関数の実行例
	// sum, err := cross(p22, board)
	// if err != nil {
	// 	fmt.Printf("Error: %v\n", err)
	// } else {
	// 	fmt.Printf("cross(p(2,2)) = %d\n", sum) // 期待値: 5 + 7 + 3 + 4 = 19
	// }

	// sum, err = cross(board.getElement(C, 1, 1), board) // C 要素
	// if err != nil {
	// 	fmt.Printf("Error: %v\n", err) // 期待: エラー
	// } else {
	// 	fmt.Printf("cross(c(1,1)) = %d\n", sum)
	// }

	// // cycle 関数の実行例
	// results := cycle(board)
	// for coord, sum := range results {
	// 	fmt.Printf("cycle at P(%d,%d) = %d\n", coord[0], coord[1], sum)
	// }

	// // その他のリストの表示例
	// // 例えば cList の中身を表示
	// fmt.Println("\n===== cList の中身 =====")
	// for _, row := range cList {
	// 	for _, elem := range row {
	// 		if elem != nil {
	// 			fmt.Printf("C(%d,%d): Value=%d\n", elem.N, elem.M, elem.Value)
	// 		}
	// 	}
	// }

	// // AbsoluteSet の例
	// totalElements := AbsoluteSet(cList)
	// fmt.Printf("\nTotal Elements in cList: %d\n", totalElements)

	// // IsSubset と IsIn の例
	// A := []int{1, 2}
	// B := []int{1, 2, 3}
	// fmt.Printf("\nIsSubset([1,2], [1,2,3]) = %v\n", IsSubset[int](A, B))
	// fmt.Printf("IsIn(2, [1,2,3]) = %v\n", IsIn[int](2, B))
	// fmt.Printf("IsIn(4, [1,2,3]) = %v\n", IsIn[int](4, B))

	// // Connect 関数の例
	// if len(cList) > 1 && len(cList[1]) > 2 {
	// 	center := cList[1][2] // C(1,2)
	// 	neighbors := Connect(center, []Relationship{H, V, D, Relationship("M")}, cList)
	// 	fmt.Printf("\ncenter = cList[1][2]: %+v\n", center)
	// 	fmt.Println("---- 隣接要素 (H or V or D or M を満たす) ----")
	// 	for _, nb := range neighbors {
	// 		fmt.Printf("%+v\n", nb)
	// 	}

	// 	// 例えば “横だけ” を拾いたい場合は
	// 	hNeighbors := Connect(center, []Relationship{H}, cList)
	// 	fmt.Printf("\n[H] 隣接のみ拾った場合:\n")
	// 	for _, nb := range hNeighbors {
	// 		fmt.Printf("%+v\n", nb)
	// 	}
	// }
}

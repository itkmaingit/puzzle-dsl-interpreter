package main

import (
	"fmt"
	"math/rand"
	"reflect"
	"time"
)

type Attribute string
type Element struct {
	Value int
	Attr  Attribute
	N     int
	M     int
}

// Element型にEqualメソッドを追加して、フィールドがすべて一致しているかを比較
func (e *Element) Equal(other *Element) bool {
	return e.Value == other.Value && e.Attr == other.Attr && e.N == other.N && e.M == other.M
}

const (
	C  = Attribute("C")
	P  = Attribute("P")
	Hp = Attribute("Hp")
	Vp = Attribute("Vp")
	Hc = Attribute("Hc")
	Vc = Attribute("Vc")

	HEIGHT = 4
	WIDTH  = 4
)

type ElementList [][]*Element

func NewElement(candicates []int, attr Attribute, n int, m int) *Element {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	// 乱数を生成(0 〜 len(targetList) - 1の範囲で)
	randIdx := r.Intn(len(candicates))
	// 対象から1つランダムに選択
	value := candicates[randIdx]
	return &Element{Value: value, Attr: attr, N: n, M: m}
}

func NewElementList(height int, width int, candidates []int, attr Attribute) ElementList {
	ret := make(ElementList, height) // height の数だけ行を作成

	// 各行について、width の数だけ Element を追加
	for i := 0; i < height; i++ {
		ret[i] = make([]*Element, width) // width の数だけ列を作成
		for j := 0; j < width; j++ {
			ret[i][j] = NewElement(candidates, attr, i, j) // ランダムに選んだ Element を代入
		}
	}
	return ret
}

func InitializeElements() (ElementList, ElementList, ElementList, ElementList, ElementList, ElementList) {

	pointCandidates := []int{0, 1, 2, 3, 4}
	edgeCandidates := []int{0, 1}
	cList := NewElementList(HEIGHT, WIDTH, pointCandidates, C)
	pList := NewElementList(HEIGHT+1, WIDTH+1, pointCandidates, P)
	hcList := NewElementList(HEIGHT, WIDTH-1, edgeCandidates, Hc)
	vcList := NewElementList(HEIGHT-1, WIDTH, edgeCandidates, Vc)
	hpList := NewElementList(HEIGHT+1, WIDTH, edgeCandidates, Hp)
	vpList := NewElementList(HEIGHT, WIDTH+1, edgeCandidates, Vp)
	return cList, pList, hcList, vcList, hpList, vpList
}

// Flatten は多次元スライス input を受け取り、一次元のスライス []T に平坦化します。
func Flatten[T any](input any) []T {
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

// IsSubset は、任意の型 T の多次元スライス A と B を受け取り、A の要素がすべて B に含まれているかを判定します。
func IsSubset[T comparable](A any, B any) bool {
	flattenedA := Flatten[T](A)
	flattenedB := Flatten[T](B)

	// B の要素をマップに収集してセットを作成
	setB := make(map[T]struct{})
	for _, elem := range flattenedB {
		setB[elem] = struct{}{}
	}

	// A の各要素が B に含まれているか確認
	for _, elem := range flattenedA {
		if _, exists := setB[elem]; !exists {
			return false
		}
	}
	return true
}

// IsIn は、任意の型 T の多次元スライス B と値 A を受け取り、
// A が B の要素として含まれているかどうかを判定します。
func IsIn[T any](A any, B any) bool {
	return isInRecursive(A, B)
}

// isInRecursive は再帰的に B を走査し、A が含まれているかを確認します。
func isInRecursive(A any, B any) bool {
	vB := reflect.ValueOf(B)

	// B がスライスでない場合、A と B を直接比較
	if vB.Kind() != reflect.Slice {
		return reflect.DeepEqual(A, B)
	}

	// B がスライスの場合、その要素を走査
	for i := 0; i < vB.Len(); i++ {
		elem := vB.Index(i).Interface()
		if reflect.DeepEqual(A, elem) {
			return true
		}

		// 要素がスライスまたは配列の場合、再帰的に検索
		kind := reflect.ValueOf(elem).Kind()
		if kind == reflect.Slice || kind == reflect.Array {
			if isInRecursive(A, elem) {
				return true
			}
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

func main() {
	c, _, _, _, _, _ := InitializeElements()
	newC := Flatten[*Element](c)
	for _, val := range newC {
		fmt.Printf("%+v\n", val)
	}
}

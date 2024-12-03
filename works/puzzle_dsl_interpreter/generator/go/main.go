package main

import (
	"fmt"
	"sync"
)

func _main() {
	numTasks := 100000
	maxWorkers := 100 // 同時に実行するゴルーチンの最大数
	var wg sync.WaitGroup
	taskChan := make(chan int, numTasks)

	// ワーカープールを作成
	for i := 0; i < maxWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range taskChan {
				cList, _, _, _, _, _ := InitializeElements()
				for i, row := range cList {
					for j, val := range row {
						fmt.Printf("c[%d][%d] = %+v\n", i, j, val)
					}
				}
			}
		}()
	}

	// タスクを送信
	for i := 0; i < numTasks; i++ {
		taskChan <- i
	}
	close(taskChan) // タスクの送信終了

	// 全てのゴルーチンの終了を待つ
	wg.Wait()
	fmt.Println("All tasks completed.")
}

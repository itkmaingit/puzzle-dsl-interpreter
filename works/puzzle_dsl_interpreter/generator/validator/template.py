from __future__ import annotations

MAIN_SCRIPT = """
package main

import (
	"fmt"
	"sync"
)

func main() {
	numTasks := 100000
	maxWorkers := 100 // 同時に実行するゴルーチンの最大数
	var wg sync.WaitGroup
	taskChan := make(chan int, numTasks)

	// ワーカープールを作成
	for i := 0; i < maxWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for _ = range taskChan {
				// 実際の処理をここで行う
				fmt.Print("")
			}
		}()
	}

	// タスクを送信
	for i := 0; i < numTasks; i++ {
		taskChan <- i
		fmt.Println(i)
	}
	close(taskChan) // タスクの送信終了

	// 全てのゴルーチンの終了を待つ
	wg.Wait()
	fmt.Println("All tasks completed.")
}


"""

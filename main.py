#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'kinoshitakenta'
__email__ = "ybs0306748@gmail.com"

"""
我只是想快一點玩完這個遊戲
之後想看看辦法能不能圖形化界面 好懶ㄛ
"""

import copy
import numpy as np
import json


def get_puzzle_data():
    # 讀取拼圖資訊
    with open ('puzzle_data.json', 'r') as f:
        puzzle_data = json.load(f)

    return puzzle_data



# 加入檢查資料型態
def input_num(msg):
    while True:
        try:
            data = int(input(msg).strip())
            return data
        except ValueError:
            print('手殘 再輸入一次\n')



# 棋盤高, 棋盤寬, 拼圖放置情形, 所有拼圖資訊, 總共有多少拼圖, 目前找出的解答
def find_next(h, w, puzzle_hash, puzzles, puzzle_put_count, ans):
    """迭代找拼圖解"""

    # 檢查拼圖是否完成
    if puzzle_put_count == len(puzzles):
        ans.append(copy.deepcopy(puzzles))
        return

    old_puzzle_hash = puzzle_hash

    # 先決定位移多少, 也就是拼圖放的位置
    for offset_h in range(h-puzzles[puzzle_put_count][0]+1):
        for offset_w in range(w-puzzles[puzzle_put_count][1]+1):
            # 檢查這個位移的位置有沒有被放過, 沒有就放下去, 然後下一步
            # print(offset_h, offset_w)
            # print(h-puzzles[puzzle_put_count][0]+1, w-puzzles[puzzle_put_count][1]+1)
            # print(puzzle_hash)
            # print(puzzles)
            next_p = False
            puzzle_hash = old_puzzle_hash

            # 檢查棋盤, 在該位置上能不能放下拼圖
            for puzzle in puzzles[puzzle_put_count][2]:
                if puzzle_hash[(puzzle[0]+offset_h, puzzle[1]+offset_w)] == 1:
                    next_p = True
                    break

            if next_p:
                continue

            # 放拼圖下去
            for puzzle in puzzles[puzzle_put_count][2]:
                puzzle_hash[(puzzle[0]+offset_h, puzzle[1]+offset_w)] = 1

            # 紀錄位移資訊
            puzzles[puzzle_put_count][3] = offset_h
            puzzles[puzzle_put_count][4] = offset_w

            # print(puzzle_hash)
            # print(puzzles)

            # 下一個迭帶
            find_next(h, w, puzzle_hash, puzzles, puzzle_put_count+1, ans)

            # 還原拼圖
            for puzzle in puzzles[puzzle_put_count][2]:
                puzzle_hash[(puzzle[0]+offset_h, puzzle[1]+offset_w)] = 0



def enter_puzzle():
    num_of_puzzle = input_num('輸入拼圖數量: ')

    puzzles = []
    puzzle_data = get_puzzle_data()


    for i in range(num_of_puzzle):
        puzzle_type = str(input_num(f'輸入第{i+1}片圖形主代號: '))
        puzzle_transform = input_num(f'輸入第{i+1}片圖形副代號: ')

        puzzle = puzzle_data[puzzle_type][puzzle_transform]
        print(puzzle)

        # [外圍高, 外圍寬, 所有拼圖, offset_h, offset_w]
        puzzles.append([puzzle['p_h'], puzzle['p_w'], puzzle['puzzle_blocks'], 0, 0])

    # print(puzzle_hash)
    # print(puzzles)
    return puzzles



if __name__ == '__main__':
    
    # 初始化棋盤
    h = input_num('輸入高: ')
    w = input_num('輸入寬: ')
    puzzle_hash = np.zeros((h, w), dtype=int)

    # 讀取該次計算所需拼圖資料
    puzzles = enter_puzzle()

    ans = []
    # 計算答案
    find_next(h, w, puzzle_hash, puzzles, 0, ans)

    # 顯示答案
    for r in ans:
        print()
        for i in r:
            print(i)

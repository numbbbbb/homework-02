#!/usr/bin/python
#coding:utf-8
import sys


movestep = [[0, -1], [1, 0], [0, 1], [-1, 0]]
allnum = []
alllen = 0
partsum = {}
visited = {}
allpoint = []
walkthrough_min_x = 0
walkthrough_min_y = 0
themax = 0
n = 0
m = 0


def resetall():                     # 重置所有变量，防止单元测试时候互相影响。
    global movestep, allnum, alllen, partsum, visited, allpoint, walkthrough_min_x, walkthrough_min_y, themax, n, m
    movestep = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    allnum = []
    alllen = 0
    partsum = {}
    visited = {}
    allpoint = []
    walkthrough_min_x = 0
    walkthrough_min_y = 0
    themax = 0
    n = 0
    m = 0


def walkthrough(x, y, tempmax):     # 递归找联通的最大值，贪心法，每次选择所有联通格子中最大的那个。
    global themax, allnum, visited, allpoint, movestep, walkthrough_min_x, walkthrough_min_y
    themax = max(themax, tempmax)
    for i in movestep:
        if x + i[0] >= walkthrough_min_x and x + i[0] < n and y + i[1] >= walkthrough_min_y and y + i[1] < m and visited[(x + i[0]) % n, (y + i[1]) % m] == 0:
            allpoint.append([(x + i[0]) % n, (y + i[1]) % m, allnum[(x + i[0]) % n][(y + i[1]) % m]])
    allpoint = sorted(allpoint, key=lambda x: x[2])
    if allpoint == []:
        return
    temptarget = [allpoint.pop()]
    while allpoint and allpoint[-1][2] == temptarget[0][2]:     # 这里是重点，如果有一样大的格子，就要分别递归。
        temptarget.append(allpoint.pop())
    for i in temptarget:
        if tempmax + i[2] > 0:   # 剪枝
            visited[i[0], i[1]] = 1
            walkthrough(i[0], i[1], tempmax + i[2])
            visited[i[0], i[1]] = 0


def main():     # 写成函数，方便单元测试。
    global allnum, alllen, partsum, visited, walkthrough_min_x, walkthrough_min_y, themax, n, m
    if len(sys.argv) < 2:      # 没有参数的情况
        raise ValueError("ERROR:You should give more args!")
    try:
        inputfile = open(sys.argv[-1], "r")
    except:
        raise IOError("ERROR:Cannot open file!")        # 文件打开错误的情况
    for line in inputfile.readlines():
        templine = [int(x) for x in line.rstrip().split(',') if x != '']
        allnum.append(templine)
        alllen += len(templine)
    inputfile.close()
    n = allnum[0][0]
    m = allnum[1][0]
    if alllen - 2 != n * m:     # 矩形尺寸于实际不符
        raise ValueError("ERROR:Matrix number doesn't match the size!")
    themax = [min([min(x) for x in allnum])][0]
    del allnum[0:2]
    if len(sys.argv) == 2:      # 无附加参数，默认情况
        for i in range(1, n + 1):
            for j in range(0, n + 1 - i):
                tempmax = 0
                if i == 1:
                    for k in range(0, m):
                        tempmax = max(tempmax + allnum[j][k], allnum[j][k])
                        themax = max(tempmax, themax)
                        partsum[k, j, 1] = allnum[j][k]
                else:
                    for k in range(0, m):
                        partsum[k, j, i] = partsum[k, j, i - 1] + allnum[j + i - 1][k]
                        tempmax = max(tempmax + partsum[k, j, i], partsum[k, j, i])
                        themax = max(tempmax, themax)
        return themax
    elif len(sys.argv) == 3:        # 有附加参数
        if sys.argv[1] == '/a':     # 联通
            for i in range(0, n):
                for j in range(0, m):
                    visited[i, j] = 0
            for i in range(0, n):
                for j in range(0, m):
                    if allnum[i][j] > 0:
                        allpoint = []
                        walkthrough_min_x = 0
                        walkthrough_min_y = 0
                        visited[i, j] = 1
                        walkthrough(i, j, allnum[i][j])
            return themax
        elif sys.argv[1] == '/h':       # 左右相连
            for i in range(1, n + 1):
                for j in range(0, n + 1 - i):
                    tempmax = 0
                    if i == 1:
                        for k in range(0, 2 * m):
                            if k > m - 1:
                                k = k % (m - 1)
                            tempmax = max(tempmax + allnum[j][k], allnum[j][k])
                            themax = max(tempmax, themax)
                            partsum[k, j, 1] = allnum[j][k]
                    else:
                        for k in range(0, 2 * m):
                            if k > m - 1:
                                k = k % (m - 1)
                            partsum[k, j, i] = partsum[k, j, i - 1] + allnum[j + i - 1][k]
                            tempmax = max(tempmax + partsum[k, j, i], partsum[k, j, i])
                            themax = max(tempmax, themax)
            return themax
        elif sys.argv[1] == '/v':       # 上下相连
            for i in range(1, n + 1):
                for j in range(0, 2 * n + 1 - i):
                    tempmax = 0
                    if i == 1:
                        for k in range(0, m):
                            tempmax = max(tempmax + allnum[j % (n - 1)][k], allnum[j % (n - 1)][k])
                            themax = max(tempmax, themax)
                            partsum[k, j, 1] = allnum[j % (n - 1)][k]
                    else:
                        for k in range(0, m):
                            partsum[k, j, i] = partsum[k, j, i - 1] + allnum[(j + i - 1) % (n - 1)][k]
                            tempmax = max(tempmax + partsum[k, j, i], partsum[k, j, i])
                            themax = max(tempmax, themax)
            return themax
        else:
            raise ValueError("ERROR:Wrong args!")
    elif len(sys.argv) == 4:        # 有两个附加参数的情况
        allargv = set(sys.argv[1:-1])
        targetargv = set(['/h', '/v'])
        if (len(allargv) == 2) and (len(allargv - targetargv) == 0):        # 左右上下都相连
            for i in range(1, n + 1):
                for j in range(0, 2 * n + 1 - i):
                    tempmax = 0
                    if i == 1:
                        for k in range(0, 2 * m):
                            if k > m - 1:
                                k = k % (m - 1)
                            tempmax = max(tempmax + allnum[j % (n - 1)][k], allnum[j % (n - 1)][k])
                            themax = max(tempmax, themax)
                            partsum[k, j, 1] = allnum[j % (n - 1)][k]
                    else:
                        for k in range(0, 2 * m):
                            if k > m - 1:
                                k = k % (m - 1)
                            partsum[k, j, i] = partsum[k, j, i - 1] + allnum[(j + i - 1) % (n - 1)][k]
                            tempmax = max(tempmax + partsum[k, j, i], partsum[k, j, i])
                            themax = max(tempmax, themax)
            return themax
        else:
            raise ValueError("ERROR:Wrong args!")
    elif len(sys.argv) == 5:        # 三个附加参数的情况
        allargv = set(sys.argv[1:-1])
        targetargv = set(['/h', '/v', '/a'])    # 左右上下相连，并且联通
        if (len(allargv) == 3) and (len(allargv - targetargv) == 0):
            for i in range(0, n):
                for j in range(0, m):
                    visited[i, j] = 0
            ok = False
            for i in range(0, n):
                if ok:
                    break
                for j in range(0, m):
                    if ok:
                        break
                    if allnum[i][j] > 0:
                        start_x = i
                        start_y = j
                        ok = True
            visited[start_x, start_y] = 1
            walkthrough_min_x = -n
            walkthrough_min_y = -m
            walkthrough(start_x, start_y, allnum[start_x][start_y])
            return themax
        else:
            raise ValueError("ERROR:Wrong args!")


if __name__ == '__main__':      # 如果直接运行此文件就执行main()函数
    print main()

import tkinter as tk
from itertools import permutations
import math
import time
import threading  

# 도시 좌표를 리스트에 저장
cities = [tuple(map(int, line.split())) for line in open("point20.txt").readlines()[1:]]

# 두 점 사이의 거리 계산
def distance(C1, C2):
    return math.sqrt((C1[0] - C2[0]) ** 2 + (C1[1] - C2[1]) ** 2)

# 경로의 총 길이 계산
def total_dis(path):
    total_dist = 0
    for i in range(len(path) - 1):
        total_dist += distance(cities[path[i] - 1], cities[path[i + 1] - 1])
    total_dist += distance(cities[path[-1] - 1], cities[path[0] - 1])  
    return total_dist

# 캔버스에 그림을 그리는 함수
def draw(canvas, path=None, message=None):
    canvas.delete("all")  
    if message:
        canvas.create_text(300, 20, text=message, font=("Arial", 16), fill="blue")  

    # 도시를 캔버스에 그리기
    for idx, city in enumerate(cities):
        canvas.create_oval(city[0] - 3, city[1] - 3, city[0] + 3, city[1] + 3, fill="black")
        canvas.create_text(city[0], city[1] - 10, text=str(idx + 1), font=("Arial", 10), fill="black")  # 도시 번호 표시
    
    # 경로가 있으면 경로를 그리기
    if path:
        for i in range(len(path) - 1):
            canvas.create_line(cities[path[i] - 1][0], cities[path[i] - 1][1], cities[path[i + 1] - 1][0], cities[path[i + 1] - 1][1], fill="red")
        canvas.create_line(cities[path[-1] - 1][0], cities[path[-1] - 1][1], cities[path[0] - 1][0], cities[path[0] - 1][1], fill="red")

    canvas.update()  

# 순열을 계산하며 최단 경로 찾기
def shortest_path(num_cities, canvas, label):
    start_city = 1 
    other_cities = list(range(2, num_cities + 1)) 
    short_path = None
    short_dist = float('inf')

    start = time.time()

    for perm in permutations(other_cities):
        path = [start_city] + list(perm)
        dist = total_dis(path)

        # 600초를 초과하면 탐색 중지하고 현재까지의 최단 경로 반환
        elapsed_time = time.time() - start
        if elapsed_time > 600:
            print(f"600초 초과, 현재까지 찾은 최단 거리: {short_dist}")
            break

        if dist < short_dist:
            short_dist = dist
            short_path = path
            label.config(text=f"최단 거리: {short_dist}")
            draw(canvas, short_path)
            canvas.update()

            # 더 좋은 경로 발견 시 경로와 거리 출력
            print(f"새로운 최단 경로 발견! 거리: {short_dist}, 경로: {short_path}")

    return short_dist, short_path, elapsed_time

# 파이썬 터미널에 출력
def play(canvas, label, num_cities):
    print(f"{num_cities}개의 도시 탐색을 시작합니다.")
    start = time.time()

    # 최단 경로 찾기
    short_dist, short_path, timer = shortest_path(num_cities, canvas, label)

    # 탐색 결과 출력
    if timer > 600:
        print(f"도시 개수: {num_cities}, 600초 초과.\n현재까지 최단 거리: {short_dist}\n최적 경로 X\n현재까지 찾은 최단 경로: {short_path}")
    else:
        print(f"도시 개수: {num_cities}, 수행 시간: {timer:.2f}초\n최단 거리: {short_dist}\n최적 경로 O\n현재까지 찾은 최단 경로: {short_path}")
    print("-" * 40)

    # 탐색 완료 메시지
    draw(canvas, short_path, message=f"{num_cities}개의 도시 탐색 완료!")
    canvas.update()

# Step 버튼 클릭 시 실행되는 함수
def playstep(canvas, label):
    global city_num
    if city_num < 20: 
        city_num += 1
        threading.Thread(target=play, args=(canvas, label, city_num)).start()
        label.config(text=f"도시 개수: {city_num}") 

# Start 버튼 클릭 시 실행되는 함수
def playstart(canvas, label):
    global city_num
    city_num = 10  # 시작 시 도시 개수를 10개로 설정
    threading.Thread(target=play, args=(canvas, label, city_num)).start()

# Tkinter GUI 설정
root = tk.Tk()
root.title("순회 외판원 문제")

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

label = tk.Label(root, text="최단 거리:")
label.pack()

# Start 버튼 설정
start_button = tk.Button(root, text="Start", command=lambda: playstart(canvas, label))
start_button.pack()

# Step 버튼 설정
step_button = tk.Button(root, text="Step", command=lambda: playstep(canvas, label))
step_button.pack()

# 도시 개수를 전역 변수 선언 및 초기화
city_num = 10

root.mainloop()




import csv
from io import StringIO
from collections import defaultdict, deque

def main(edges_str: str, root_id_str: str) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    graph = defaultdict(list)
    nodes = set()
    
    file_content = edges_str.strip()
    csv_reader = csv.reader(StringIO(file_content))
    
    for row in csv_reader:
        if len(row) < 2:
            continue
        u, v = row[0].strip(), row[1].strip()
        if not u or not v:
            continue
        graph[u].append(v)
        nodes.add(u)
        nodes.add(v)
    
    if root_id_str not in nodes:
        nodes.add(root_id_str)

    other_nodes = sorted([n for n in nodes if n != root_id_str])
    node_list = [root_id_str] + other_nodes
    n = len(node_list)

    parent = {node: None for node in node_list}
    ancestors = defaultdict(set)
    
    q = deque([root_id_str])
    visited = {root_id_str}
    
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                ancestors[v].add(u)
                ancestors[v].update(ancestors[u])
                q.append(v)

    gamma1 = [[0] * n for _ in range(n)]
    gamma2 = [[0] * n for _ in range(n)]
    gamma3 = [[0] * n for _ in range(n)]
    gamma4 = [[0] * n for _ in range(n)]
    gamma5 = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            u = node_list[i]
            v = node_list[j]

            if parent[v] == u:
                gamma1[i][j] = 1

            if parent[u] == v:
                gamma2[i][j] = 1

            if u in ancestors[v] and parent[v] != u:
                gamma3[i][j] = 1

            if v in ancestors[u] and parent[u] != v:
                gamma4[i][j] = 1
            
            if i != j and parent[u] is not None and parent[u] == parent[v]:
                gamma5[i][j] = 1

    return (gamma1, gamma2, gamma3, gamma4, gamma5)

if __name__ == '__main__':
    
    path = 'task0/data.csv'
    with open(path, 'r') as file:
        csv_data = file.read()
    root = "1"
    
    matrices = main(csv_data, root)
    
    g1, g2, g3, g4, g5 = matrices
    
    print("Матрица Г1 (Управляет):")
    for row in g1:
        print(row)
    print("\nМатрица Г2 (Подчиняется):")
    for row in g2:
        print(row)
    print("\nМатрица Г3 (Опосредованно управляет):")
    for row in g3:
        print(row)
    print("\nМатрица Г4 (Опосредованно подчиняется):")
    for row in g4:
        print(row)
    print("\nМатрица Г5 (Соподчинение):")
    for row in g5:
        print(row)

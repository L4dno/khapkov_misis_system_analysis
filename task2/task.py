import typing
import io
import csv
import math

def task(csv_data: str, root: str) -> typing.Tuple[float, float]:

    def partial_entropy(p: float) -> float:
        if p <= 0.0:
            return 0.0
        return -p * math.log2(p)

    adj = {}
    nodes = set()

    try:
        f = io.StringIO(csv_data)
        reader = csv.reader(f)
        
        for row in reader:
            if not row or len(row) < 2:
                continue
            
            u, v = row[0].strip(), row[1].strip()

            if not u or not v:
                continue

            if u not in adj:
                adj[u] = []
            adj[u].append(v)
            
            nodes.add(u)
            nodes.add(v)
            
    except Exception as e:
        print(f"Ошибка при парсинге CSV: {e}")
        return (0.0, 0.0)

    n = len(nodes)
    
    if n <= 1:
        return (0.0, 0.0)

    r = {f'r{i}': set() for i in range(1, 6)} 

    for u in nodes:
        if u not in adj: 
            continue
        
        children = adj[u]
        
        for v in children:
            r['r1'].add((u, v))
            r['r2'].add((v, u))
            
            if v in adj:
                grandchildren = adj[v]
                for w in grandchildren:
                    r['r3'].add((u, w))
                    r['r4'].add((w, u))

        for i in range(len(children)):
            for j in range(i + 1, len(children)):
                c1, c2 = children[i], children[j]
                r['r5'].add((c1, c2))
                r['r5'].add((c2, c1))
                
    k = 5

    l_counts = {node: {f'r{i}': 0 for i in range(1, 6)} for node in nodes}
    
    for i in range(1, k + 1):
        r_name = f'r{i}'
        for u_rel, v_rel in r[r_name]:
            if u_rel in l_counts:
                l_counts[u_rel][r_name] += 1

    max_links = n - 1
    total_entropy = 0.0
    
    for node in nodes:
        node_entropy = 0.0
        for i in range(1, k + 1):
            r_name = f'r{i}'
            
            l_ij = l_counts[node].get(r_name, 0)
            
            p = 0.0
            if max_links > 0:
                p = l_ij / max_links
            
            h_ij = partial_entropy(p)
            node_entropy += h_ij
            
        total_entropy += node_entropy
        
    H = total_entropy

    c = 1 / (math.e * math.log(2)) 
    
    H_ref = c * n * k
    
    h = 0.0
    if H_ref > 0:
        h = H / H_ref
    
    return (round(H, 1), round(h, 1))


if __name__ == '__main__':
    
    path = 'task0/data.csv'
    with open(path, 'r') as file:
        csv_data = file.read()
    root = "1"
        
    H_file, h_file = task(csv_data, root)
    print(f"Энтропия: {H_file}")
    print(f"Структурная сложность: {h_file}")

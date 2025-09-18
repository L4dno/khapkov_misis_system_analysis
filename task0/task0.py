import csv
from io import StringIO

def main(csv_graph: str) -> list[list[int]]:
    """
    Строит матрицу смежности ориентированного графа из строки CSV.

    Args:
        csv_graph: Строка, содержащая данные графа в формате CSV.
                   Каждая строка представляет собой ребро: начальная_вершина,конечная_вершина.

    Returns:
        Матрица смежности графа в виде списка списков.
    """

    data_stream = StringIO(csv_graph)
    reader = csv.reader(data_stream)

    vertices = set()
    edges = []
    for row in reader:
        if len(row) == 2:
            start_node = int(row[0])
            end_node = int(row[1])
            vertices.add(start_node)
            vertices.add(end_node)
            edges.append((start_node, end_node))

    sorted_vertices = sorted(list(vertices))
    num_vertices = len(sorted_vertices)

    vertex_to_index = {vertex: i for i, vertex in enumerate(sorted_vertices)}

    adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    for start_node, end_node in edges:
        start_index = vertex_to_index[start_node]
        end_index = vertex_to_index[end_node]
        adj_matrix[start_index][end_index] = 1

    return adj_matrix


path = 'task0/data.csv'
with open(path, 'r') as file:
    csv_data = file.read()

result = main(csv_data)
print("Матрица смежности:")
for row in result:
    print(row)

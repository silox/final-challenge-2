from collections import deque


def insert_edge(graph, from_node, to_node):
    graph[from_node].add(to_node)
    graph[to_node].add(from_node)


def bfs(graph, from_node, to_node):
    queue = deque([(from_node, 0)])
    visited = {from_node}
    while queue:
        node, dist = queue.popleft()
        if node == to_node:
            return dist
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, dist + 1))
    return -1


def main():
    nodes, edges = map(int, input().split())
    source, destination, connector = map(int, input().split())
    graph = {node: set() for node in range(nodes)}
    for i in range(edges):
        insert_edge(graph, *map(int, input().split()))
    source_to_connector = bfs(graph, source, connector)
    connector_to_destination = bfs(graph, connector, destination)
    return -1 if source_to_connector == -1 or connector_to_destination == -1 else source_to_connector + connector_to_destination


print(main())

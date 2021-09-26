import openpyxl


wb = openpyxl.load_workbook('distance.xlsx')
sheet = wb.active # Only one sheet anyway

nodes = set()
edges = []
for row in range(2, sheet.max_row): # Row 1 is destinations so start at 2
    source = str(sheet[row][0].value)
    nodes.add(source)

    for col in range(1, row): # Col 0 is the source so start at 1
        distance = sheet[row][col].value
        destination = sheet[1][col].value
        
        if distance == 0 or distance == None:
            break # Skip self or empty cells.
        else:
            edges.append((source, distance, destination))

wb.close()

with open('nodes.txt', 'w') as node_file:
    for node in sorted(nodes):
        node_file.write(node + "\n")

with open('edges.csv', 'w') as edge_file:
    for edge in edges:
        edge_file.write("{},{},{}\n".format(edge[0],edge[1],edge[2]))

print('Done')

DMIN = -100
DMAX = 100
count = 10

def make_slabs(slabs, xcoords):
    rhs = DMIN
    for i in range(len(xcoords)):
        lhs = rhs
        rhs = xcoords[i]
        slabs.append((lhs, rhs))
    slabs.append((rhs, DMAX))
    return

def calcY(begLine, endLine, x):
    y = (x - begLine[0]) * (endLine[1] - begLine[1])
    y = y / (endLine[0] - begLine[0])
    y = y + begLine[1]
    return y

def bsRec(slabs, p, beg, end):
    global count
    mid = int((beg + end)/2)
    if count < 10:
        print(beg, ' ', mid, ' ', end, ' ')
        count = count + 1
    if (slabs[mid][0] <= p[0] and slabs[mid][1] > p[0]):
        return mid
    elif (slabs[mid][0] > p[0]):
        return bsRec(slabs, p, beg, mid - 1)
    return bsRec(slabs, p, mid + 1, end)

def bs(slabs, p):
    return bsRec(slabs, p, 0, len(slabs) - 1)

def remove_doubles(l):
    ret = []
    for x in range (len(l) - 1):
        if l[x] != l[x + 1]:
            ret.append(l[x])
    ret.append(l[len(l) - 1])
    return ret

def hor_lines_key(l):
    return [l[0], l[1], -l[2]]

def add_line(lines, slabs, beg, end, pNum):
    if (beg[0] < end[0]):
        aux = pNum
    else:
        aux = -1
        auxp = (beg[0], beg[1])
        beg = (end[0], end[1])
        end = (auxp[0], auxp[1])
    
    for i in range (bs(slabs, beg), bs(slabs, end)):
        lines[i].append((calcY(beg, end, slabs[i][0]), calcY(beg, end, slabs[i][1]), aux))
    return

def make_lines(lines, slabs, polygons):
    for i in range (len(polygons)):
        for j in range (len(polygons[i])):
            add_line(lines, slabs, polygons[i][j], polygons[i][(j + 1) % len(polygons[i])], i)
    for i in range (len(slabs)):
        lines[i].append((DMAX, DMAX, -1))
        lines[i].sort(key = hor_lines_key)
        lines[i] = remove_doubles(lines[i])
    return

def esquerda(X1, Y1, X2, Y2, X3, Y3):
    return ((X2 - X1) * (Y3 - Y1) - (X3 - X1) * (Y2 - Y1) >= 0)

def bsPointLines(lines, slab, p, beg, end):
    mid = int((beg + 1 + end)/2)
    if (mid == beg):
        return mid
    if (esquerda(slab[0], lines[mid][0], slab[1], lines[mid][1], p[0], p[1])):
        return bsPointLines(lines, slab, p, mid + 1, end)
    if (not esquerda(slab[0], lines[mid - 1][0], slab[1], lines[mid - 1][1], p[0], p[1])):
        return bsPointLines(lines, slab, p, beg, mid - 1)
    return mid

def main():
    line = input()
    parsed = line.split()
    N = int(parsed[0])
    polygons = []
    xcoords = []
    for i in range (N):
        line = input()
        parsed = line.split()
        sz = int(parsed[0])
        polygons.append([])
        for j in range (sz):
            line = input()
            parsed = line.split()
            a = float(parsed[0])
            b = float(parsed[1])
            polygons[i].append((a, b))
            xcoords.append(a)
    xcoords.sort()
    xcoords = remove_doubles(xcoords)

    slabs = []
    make_slabs(slabs, xcoords)
    
    lines = []
    for i in range (len(slabs)):
        lines.append([])
    make_lines(lines, slabs, polygons)
    
    line = input()
    parsed = line.split()
    numP = int(parsed[0])
    points = []
    for i in range (numP):
        line = input()
        parsed = line.split()
        a = float(parsed[0])
        b = float(parsed[1])
        points.append((a, b))
    
    for i in range (numP):
        s = bs(slabs, points[i])
        l = bsPointLines(lines[s], slabs[s], points[i], 0, len(lines[s]) - 1)
        print(lines[s][l][2])
    return
    
main()
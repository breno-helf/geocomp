from copy import deepcopy

DMIN = -100
DMAX = 100
count = 10

def esquerda(X1, Y1, X2, Y2, X3, Y3):
    return ((X2 - X1) * (Y3 - Y1) - (X3 - X1) * (Y2 - Y1) >= 0)

class Event(object):
    beg = [0.0, 0.0]
    end = [0.0, 0.0]
    insert = True
    polygon = -2
    
    def __init__(self, beg, end, ins, p):
        self.beg[0] = beg[0]
        self.beg[1] = beg[1]
        self.end[0] = end[0]
        self.end[1] = end[1]
        self.insert = ins
        self.polygon = p


class HorLine(object):
    
    def __init__(self, val):
        self.beg = []
        self.end = []
        self.beg.append(val[0])
        self.beg.append(val[1])
        self.end.append(val[2])
        self.end.append(val[3])
        self.polygon = val[4]
        
    def __eq__(self, other):
        if (self.beg[0] == other.beg[0] and self.beg[1] == other.beg[1]):
            if (self.end[0] == other.end[0] and self.end[1] == other.end[1]):
                return (self.polygon == other.polygon)
        return False
    
    def __ne__(self, other):
        return not (self == other)
    
    def __lt__(self, other):
        if (self.beg[0] == other.beg[0] and self.beg[1] == other.beg[1]):
            if (self.end[0] == other.end[0] and self.end[1] == other.end[1]):
                return (self.polygon > other.polygon)
        b1 = esquerda(other.beg[0], other.beg[1], other.end[0], other.end[1], self.beg[0], self.beg[1])
        b2 = esquerda(other.beg[0], other.beg[1], other.end[0], other.end[1], self.end[0], self.end[1])
        if (b1 and b2):
            return False
        if (not b1 and not b2):
            return True
        b1 = esquerda(self.beg[0], self.beg[1], self.end[0], self.end[1], other.beg[0], other.beg[1])
        b2 = esquerda(self.beg[0], self.beg[1], self.end[0], self.end[1], other.end[0], other.end[1])
        if (b1 and b2):
            return True
        return False
        
    def __le__(self, other):
        if (self == other or self < other):
            return true
        return false

    def __gt__(self, other):
        return (other < self)
    
    def __ge__(self, other):
        return (other <= self)

def print_HorLine(hl):
    print("beg = ", end = "")
    print(hl.beg[0], end = " ")
    print(hl.beg[1])
    print("end = ", end = "")
    print(hl.end[0], end = " ")
    print(hl.end[1])
    print("poly = ", end = "")
    print(hl.polygon)
    return


# AVL code, based on the geeks for geeks version:
# https://www.geeksforgeeks.org/avl-tree-set-2-deletion/ 

class TreeNode(object): 
    def __init__(self, key, val):
        self.key = key
        self.val = val 
        self.left = None
        self.right = None
        self.height = 1

# AVL tree class which supports insertion, 
# deletion operations 
class AVL_Tree(object): 

    def find(self, root, key):
        if not root:
            return False
        elif key == root.key:
            return root.val
        elif key < root.key:
            return self.find(root.left, key)
        else:
            return self.find(root.right, key)

    def insert(self, root, key, val): 
        
        # Step 1 - Perform normal BST 
        if not root: 
            return TreeNode(key, val) 
        elif key < root.key: 
            root.left = self.insert(root.left, key, val) 
        else: 
            root.right = self.insert(root.right, key, val) 

        # Step 2 - Update the height of the 
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                        self.getHeight(root.right)) 

        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 

        # Step 4 - If the node is unbalanced, 
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and key < root.left.key: 
            return self.rightRotate(root) 

        # Case 2 - Right Right 
        if balance < -1 and key > root.right.key: 
            return self.leftRotate(root) 

        # Case 3 - Left Right 
        if balance > 1 and key > root.left.key: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 

        # Case 4 - Right Left 
        if balance < -1 and key < root.right.key: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 

        return root 

    # Recursive function to delete a node with 
    # given key from subtree with given root. 
    # It returns root of the modified subtree. 
    def delete(self, root, key): 

        # Step 1 - Perform standard BST delete 
        if not root: 
            return root 

        elif key < root.key: 
            root.left = self.delete(root.left, key) 

        elif key > root.key: 
            root.right = self.delete(root.right, key) 

        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 

            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 

            temp = self.getMinValueNode(root.right) 
            root.key = temp.key 
            root.val = temp.val
            root.right = self.delete(root.right, 
                                    temp.key) 

        # If the tree has only one node, 
        # simply return it 
        if root is None: 
            return root 

        # Step 2 - Update the height of the 
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 

        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 

        # Step 4 - If the node is unbalanced, 
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.rightRotate(root) 

        # Case 2 - Right Right 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.leftRotate(root) 

        # Case 3 - Left Right 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 

        # Case 4 - Right Left 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 

        return root 

    def leftRotate(self, z): 

        y = z.right 
        T2 = y.left 

        # Perform rotation 
        y.left = z 
        z.right = T2 

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 

        # Return the new root 
        return y 

    def rightRotate(self, z): 

        y = z.left 
        T3 = y.right 

        # Perform rotation 
        y.right = z 
        z.left = T3 

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 

        # Return the new root 
        return y 

    def getHeight(self, root): 
        if not root: 
            return 0

        return root.height 

    def getBalance(self, root): 
        if not root: 
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right) 

    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 

        return self.getMinValueNode(root.left) 

    def inOrder(self, root): 

        if not root: 
            return []
        
        v = []
        v.extend(self.inOrder(root.left))
        v.append((root.key, root.val)) 
        v.extend(self.inOrder(root.right))
        return v

    def printPreOrder(self, root): 
  
        if not root: 
            return
  
        print("{0} ".format(root.val), end="") 
        self.printPreOrder(root.left) 
        self.printPreOrder(root.right) 

def make_events(polygons):
    evts = AVL_Tree()
    root = None
    lp = [0.0, 0.0]
    rp = [0.0, 0.0]
    
    lb = []
    
    for i in range (len(polygons)):
        for j in range (len(polygons[i])):
            lp = []
            rp = []
            if (polygons[i][j][0] < polygons[i][(j + 1) % len(polygons[i])][0]):
                lp.append(polygons[i][j][0])
                lp.append(polygons[i][j][1])
                rp.append(polygons[i][(j + 1) % len(polygons[i])][0])
                rp.append(polygons[i][(j + 1) % len(polygons[i])][1])
                poly = i
            else:
                lp.append(polygons[i][j][0])
                lp.append(polygons[i][j][1])
                rp.append(polygons[i][(j + 1) % len(polygons[i])][0])
                rp.append(polygons[i][(j + 1) % len(polygons[i])][1])
                poly = -1
            b = Event(lp, rp, True, poly)
            e = Event(lp, rp, False, poly)
            b.beg[0] = e.beg[0] = lp[0]
            b.beg[1] = e.beg[1] = lp[1]
            b.end[0] = e.end[0] = rp[0]
            b.end[1] = e.end[1] = rp[1]
            b.insert = True
            e.insert = False
            b.polygon = e.polygon = poly
            if (evts.find(root, lp[0]) == False):
                root = evts.insert(root, lp[0], [])
            
            #(evts.find(root, lp[0])).append(b)
            (evts.find(root, lp[0])).append(Event(lp, rp, True, poly))
            if (evts.find(root, rp[0]) == False):
                root = evts.insert(root, rp[0], [])
            #(evts.find(root, rp[0])).append(e)
            (evts.find(root, lp[0])).append(Event(lp, rp, False, poly))
            
    return root

def print_event(evt):
    print("x coord = ", end = "")
    print(evt[0])
    print("events = ")
    for i in range (len(evt[1])):
        print(evt[1][i].beg[0], end = ", ")
        print(evt[1][i].beg[1])
        print(evt[1][i].end[0], end = ", ")
        print(evt[1][i].end[1])
        if (evt[1][i].insert):
            print("insert")
        else:
            print("remove")
        print("poly = ", end = "")
        print(evt[1][i].polygon)
        

class Slab(object):
    beg = 0.0
    end = 0.0
    lines = []

def print_slab(s):
    print("beg = ", end = "")
    print(s.beg)
    print("end = ", end = "")
    print(s.end)
    for i in range (len(s.lines)):
        print_HorLine(s.lines[i])
    print("####################################")
    return

def make_slab(slab, abb, root):
    curr = deepcopy(slab)
    v = []
    abb.inOrder(root, v)
    for i in range (len(v)):
        curr.lines.append(v[i][0])
    return curr
    
def update_abb(abb, root, el):
    l = HorLine([el.beg[0], el.beg[1], el.end[0], el.end[1], el.polygon])
    if el.insert:
        root = abb.insert(root, l, [])
    else:
        root = abb.delete(root, l)
    return root

def make_slabs(s, events, root):
    abb = AVL_Tree()
    abb_Root = None
    curr = Slab()
    cel = HorLine([DMIN, DMAX, DMAX, DMAX, -1])
    abb_Root = abb.insert(abb_Root, cel, [])
    curr.end = DMIN
    v = events.inOrder(root)
    
    for i in range(len(v)):
        curr.beg = curr.end
        curr.end = v[i][0]
        s.append(make_slab(curr, abb, abb_Root))
        for j in range (len(v[i][1])):
            if not v[i][1][j].insert:
                abb_Root = update_abb(abb, abb_Root, v[i][1][j])
        for j in range (len(v[i][1])):
            if v[i][1][j].insert:
                abb_Root = update_abb(abb, abb_Root, v[i][1][j])
        curr.beg = curr.end
        curr.end = DMAX
        s.append(make_slab(curr, abb, abb_Root))
    
def bs(s, p):
    beg = 0
    end = len(s) - 1
    while beg < end:
        mid1 = (beg + end) // 2
        if s[mid1].beg > p[0]:
            end = mid1 - 1
        elif s[mid1].end <= p[0]:
            beg = mid1 + 1
        else:
            beg = end = mid1
    mid1 = beg
    
    beg = 0
    end = len(s[mid1].lines) - 1
    while beg < end:
        mid2 = (beg + end) // 2
        if esquerda(s[mid1].lines[mid2].beg[0], s[mid1].lines[mid2].beg[1], s[mid1].lines[mid2].end[0], s[mid1].lines[mid2].end[1], p[0], p[1]):
            beg = mid2 + 1
        else:
            end = mid2
    mid2 = beg
    
    return s[mid1].lines[mid2].polygon

def main():
    line = input()
    parsed = line.split()
    N = int(parsed[0])
    polygons = []
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
    
    events = AVL_Tree()
    eventsRoot = make_events(polygons)
    
    v = events.inOrder(eventsRoot)
    for i in range(len(v)):
        print_event(v[i])
    
    s = []
    make_slabs(s, events, eventsRoot)
    
    #for i in range(len(s)):
    #    print_slab(s[i])
    
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
        print(bs(s, points[i]))
    return

main()
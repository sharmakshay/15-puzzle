from graphics import *
import random

# CONSTANTS
win = GraphWin("15 Puzzle", 400, 400)

# draw close button
close = Rectangle(Point(320, 370), Point(400, 400))
close.draw(win)
closeLabel = Text(Point(360, 385), "X CLOSE")
closeLabel.draw(win)
windowopen = True

# draw solve button to initiate A*
solve = Rectangle(Point(5, 370), Point(85, 400))
solve.draw(win)
solveLabel = Text(Point(45, 385), "SOLVE")
solveLabel.draw(win)
astarInit = False

goal = {"00": 1, "01": 2, "02": 3, "03": 4, "10": 5, "11": 6, "12": 7, "13": 8, "20": 9, "21": 10, "22": 11,
        "23": 12, "30": 13, "31": 14, "32": 15, "33": ""}

key = ["00", "01", "02", "03", "10", "11", "12", "13", "20", "21", "22", "23", "30", "31", "32", "33"]
value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ""]


# VARIABLES

# dictionary to store label for each cell, retrieved later to change label text during swap
labels = {}

# dictionary to store current grid
numbers = {}

# array to store all cell IDs adjacent to the empty cell
adjacent = []

# shuffle array each time program is run, in order to get a different puzzle every time
random.shuffle(value)

# stores ID of current empty space index in grid
emptyspace = ""
count = 0
col, row = 0, 0

# used during A*
alt = {}
options = {}

# two variables that determine cost for a step in A* -- f(x) = g(x) + h(x)
gx = 0
hx = 0


# put shuffled values with keys in dictionary
for a in range(0, 16):
    numbers.update({key[a]: value[a]})


# draws grid
def drawGrid():
    # initial coordinates of first square
    a1, b1, a2, b2 = 100, 50, 150, 100

    # draws a grid of 4x4 squares
    for i in range(0, 4):
        for j in range(0, 4):
            square(a1, b1, a2, b2)
            a1 += 50
            a2 += 50

        b1 += 50
        b2 += 50
        a1 = 100
        a2 = 150


# draws a square and its label with given coordinates
def square(x1, y1, x2, y2):
    global count
    global col
    global row

    s = Rectangle(Point(x1, y1), Point(x2, y2))
    lx = (x1 + x2) / 2
    ly = (y1 + y2) / 2

    convert(x1, y1)

    labelid = row+col
    label = Text(Point(lx, ly), numbers.get(key[count]))
    labels.update({labelid: label})

    s.draw(win)
    label.draw(win)

    count += 1


# converts given x and y coordinates to square ID (row and column)
def convert(x, y):
    global col
    global row

    col = str(int((x-100)/50))
    row = str(int((y-50)/50))


# finds where current empty value is located in grid
def findemptyspace():
    global emptyspace
    global numbers

    for b in numbers:
        currVal = numbers.get(b)
        if not(isinstance(currVal, int)):
            emptyspace = b
            break


# CODE: sets adjacent values based on the white spaces
# USER: determines which cells user can swap for empty cell
def setadjacent():
    global emptyspace
    global adjacent

    r = int(emptyspace[0])
    c = int(emptyspace[1])

    a = r-1
    b = c-1

    e = r+1
    f = c+1

    if a < 0:
        a = 0

    if b < 0:
        b = 0

    if e > 3:
        e = 3

    if f > 3:
        f = 3

    for i in range(a, e+1):
        for j in range(b, f+1):
            id = str(i) + str(j)
            adjacent.append(id)


# CODE: swap the value of two given keys in dictionary
# USER: swaps value of cell user clicks with empty cell
def swap(keyClick):
    global numbers
    global labels
    global emptyspace

    temp = numbers.get(keyClick)
    numbers[keyClick] = ""
    numbers[emptyspace] = temp

    labels.get(keyClick).setText("")
    labels.get(emptyspace).setText(temp)


# swap function for A*
def astarswap(cid):
    global numbers
    global labels
    global emptyspace

    temp = alt.get(cid)
    alt[cid] = ""
    alt[emptyspace] = temp
    cost(cid)


# finds cost of one alternative given cell id
def cost(cellid):
    global emptyspace
    global alt
    global goal
    global gx
    global hx

    if emptyspace[0] == cellid[0] or emptyspace[1] == cellid[1]:
        gx = 1

    else:
        gx = 1.5

    hx = 0
    fx = 0
    for cell in alt:
        val = alt.get(cell)
        for goalCell in goal:
            valGoal = goal.get(goalCell)
            if valGoal == val:
                gCell = goalCell
                break
        b = abs(int(cell[0]) - int(gCell[0]))
        a = abs(int(cell[1]) - int(gCell[1]))
        dist = b+a
        hx += dist

    fx = gx + hx

    options.update({cellid: fx})


def main():
    global adjacent
    global alt
    global numbers
    global goal
    global astarInit
    global options

    drawGrid()

    # while user does not click the close button
    while windowopen:

        if numbers == goal:
            success = Text(Point(190, 385), "YOU WON!")
            success.setStyle('bold')
            success.setTextColor('green')
            success.setSize(20)
            success.draw(win)

        # get mouse click coordinates
        mouseclick = win.getMouse()
        mouseX = mouseclick.getX()
        mouseY = mouseclick.getY()

        # CLOSE WINDOW -- if user clicks close button exit loop
        if 320 < mouseX < 400 and 370 < mouseY < 400:
            break

        # INITIATE A* -- if solve button is clicked
        if 5 < mouseX < 85 and 370 < mouseY < 400:
            astarInit = True
            while not(numbers == goal):
                adjacent = []
                findemptyspace()
                setadjacent()
                for i in adjacent:
                    alt = numbers
                    astarswap(i)

                min = 0
                print(options)
                for l in options:
                    optcost = options.get(l)
                    if min > optcost:
                        min = l

                swap(l)

        # USER PLAYING -- if close nor solve buttons are clicked, then user is playing
        else:
            global count

            adjacent = []
            findemptyspace()
            setadjacent()

            '''
            print(numbers)
            print(emptyspace)
            '''

            convert(mouseX, mouseY)
            sqid = str(row) + str(col)
            count = 0
            if sqid in adjacent:
                swap(sqid)

            '''
            print(row)
            print(col)
            print(numbers.get(row+col))
            print(adjacent)
            print(numbers)
            '''

main()
win.close()

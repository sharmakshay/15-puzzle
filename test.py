from graphics import *

win = GraphWin("Test Window", 400, 400)


def main():
    label = Text(Point(200, 200), "skjhdaos")
    label.draw(win)
    label.setText(" ")
    win.getMouse()
    win.close()

main()



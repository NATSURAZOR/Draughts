import tkinter
from PIL import Image, ImageTk


class Gamers:
    def __init__(self):
        self.gamer1 = False
        self.gamer2 = False
        self.gamer1WantoDraw = False
        self.gamer2WnatToDraw = False

    def swapturn(self):
        if self.gamer1:
            self.gamer1 = False
            self.gamer2 = True
            return

        if self.gamer2:
            self.gamer2 = False
            self.gamer1 = True
            return

    def turn(self):
        img = ''

        if self.gamer1:
            img = Image.open('sprites/whiteFigure/whiteTurn.png')

        if self.gamer2:
            img = Image.open('sprites/blackFigure/blackTurn.png')

        img = img.resize((250, 150))
        imgtk = ImageTk.PhotoImage(img)
        return imgtk


class Color(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Empty(object):
    color = Color.EMPTY

    def __init__(self, matrixPos, size, pozition):
        self.matrixPos = matrixPos
        self.size = size
        self.pozition = pozition
        self.id = ''

    def inside(self, x, y):
        return (self.pozition[0] - x + self.size[0] / 2) ** 2 + (self.pozition[1] - y + self.size[1] / 2) ** 2 \
               <= (self.size[0] / 2) ** 2

    def getMoves(self, board, x, y):
        return ([x, y], None)

    def move(self, x, y):
        return

    def __repr__(self):
        return '.'


class Figure(object):
    figure = None

    def __init__(self, color, matrixPos, size, pozition):
        self.color = color
        self.matrixPos = matrixPos
        self.size = size
        self.pozition = pozition
        self.id = ''

    def __repr__(self):
        return self.figure[0 if self.color == Color.WHITE else 1]

    def inside(self, x, y):
        return (self.pozition[0] - x + self.size[0] / 2) ** 2 + (self.pozition[1] - y + self.size[1] / 2) ** 2 \
               <= (self.size[0] / 2) ** 2

    def move(self, x, y):
        self.canvas.move(self.id, x - self.pozition[0], y - self.pozition[1])
        self.pozition = (x, y)


class Draught(Figure):
    figure = ('⛀', '⛂')

    def __init__(self, color, matrixPos, size, pozition):
        super().__init__(color, matrixPos, size, pozition)
        imgName = 'whiteFigure/white'
        if color == 1:
            imgName = 'blackFigure/black'

        self.image = Image.open(f'sprites/{imgName}.png').resize(size)
        self.image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(pozition[0], pozition[1], image=self.image, anchor='nw')

    def getMoves(self, board, x, y):
        nonAttackposition = None
        attackPosition = [None, None]

        def checkPosition(board, row, col, color):
            if row in range(8) and col in range(8) and board.getColor(row, col) == color:
                return True
            return False

        def attackFigure(board, x, y, enemyColor):
            attackArr = []

            if checkPosition(board, x + 1, y + 1, enemyColor) and checkPosition(board, x + 2, y + 2, Color.EMPTY):
                attackPosition = [x + 1, y + 1]
                attackArr.append(([x + 2, y + 2], attackPosition))

            if checkPosition(board, x + 1, y - 1, enemyColor) and checkPosition(board, x + 2, y - 2, Color.EMPTY):
                attackPosition = [x + 1, y - 1]
                attackArr.append(([x + 2, y - 2], attackPosition))

            if checkPosition(board, x - 1, y + 1, enemyColor) and checkPosition(board, x - 2, y + 2, Color.EMPTY):
                attackPosition = [x - 1, y + 1]
                attackArr.append(([x - 2, y + 2], attackPosition))

            if checkPosition(board, x - 1, y - 1, enemyColor) and checkPosition(board, x - 2, y - 2, Color.EMPTY):
                attackPosition = [x - 1, y - 1]
                attackArr.append(([x - 2, y - 2], attackPosition))

            return attackArr

        def nonAttackFigure(board, x, y):
            nonAttackArr = []

            if checkPosition(board, x + 1, y + 1, Color.EMPTY) and board.getColor(x, y) == Color.BLACK:
                nonAttackArr.append(([x + 1, y + 1], nonAttackposition))

            if checkPosition(board, x + 1, y - 1, Color.EMPTY) and board.getColor(x, y) == Color.BLACK:
                nonAttackArr.append(([x + 1, y - 1], nonAttackposition))

            if checkPosition(board, x - 1, y + 1, Color.EMPTY) and board.getColor(x, y) == Color.WHITE:
                nonAttackArr.append(([x - 1, y + 1], nonAttackposition))

            if checkPosition(board, x - 1, y - 1, Color.EMPTY) and board.getColor(x, y) == Color.WHITE:
                nonAttackArr.append(([x - 1, y - 1], nonAttackposition))

            return nonAttackArr

        moves = []

        if board.getColor(x, y) == Color.BLACK:
            moves = attackFigure(board, x, y, Color.WHITE)

        if board.getColor(x, y) == Color.WHITE:
            moves = attackFigure(board, x, y, Color.BLACK)

        if moves is None or len(moves) == 0:
            moves = nonAttackFigure(board, x, y)

        return moves


class DraughtQuin(Figure):
    figure = ('⛁', '⛃')

    def __init__(self, color, matrixPos, size, pozition):
        super().__init__(color, matrixPos, size, pozition)
        imgName = 'whiteFigure/damaWhite'
        if color == 1:
            imgName = 'blackFigure/damaBlack'

        self.image = Image.open(f'sprites/{imgName}.png').resize(size)
        self.image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(pozition[0], pozition[1], image=self.image, anchor='nw')
        print(matrixPos)

    def getMoves(self, board, x, y):

        def checkPosition(board, row, col, color):
            if row in range(8) and col in range(8) and board.getColor(row, col) == color:
                return True
            return False

        def nonAttackFigure(board, x, y):
            nonAttackArr = []
            nonAttackPosition = None

            for i in range(1, 8):
                if checkPosition(board, x + i, y + i, Color.EMPTY):
                    nonAttackArr.append(([x + i, y + i], nonAttackPosition))
                else:
                    break

            for i in range(1, 8):
                if checkPosition(board, x + i, y - i, Color.EMPTY):
                    nonAttackArr.append(([x + i, y - i], nonAttackPosition))
                else:
                    break

            for i in range(1, 8):
                if checkPosition(board, x - i, y + i, Color.EMPTY):
                    nonAttackArr.append(([x - i, y + i], nonAttackPosition))
                else:
                    break

            for i in range(1, 8):
                if checkPosition(board, x - i, y - i, Color.EMPTY):
                    nonAttackArr.append(([x - i, y - i], nonAttackPosition))
                else:
                    break

            return nonAttackArr

        def attackFigure(board, x, y, enemyColor):
            attackArr = []
            attackPosition = [None, None]

            t1 = False
            for i in range(1, 8):
                if checkPosition(board, x + i, y + i, enemyColor):
                    t1 = True
                    attackPosition = [x + i, y + i]
                if checkPosition(board, x + i + 1, y + i + 1, Color.EMPTY) and t1:
                    attackArr.append(([x + i + 1, y + i + 1], attackPosition))
                if t1 and not checkPosition(board, x + i + 1, y + i + 1, Color.EMPTY):
                    break

            t1 = False
            for i in range(1, 8):
                if checkPosition(board, x + i, y - i, enemyColor):
                    t1 = True
                    attackPosition = [x + i, y - i]
                if checkPosition(board, x + i + 1, y - i - 1, Color.EMPTY) and t1:
                    attackArr.append(([x + i + 1, y - i - 1], attackPosition))
                if t1 and not checkPosition(board, x + i + 1, y - i - 1, Color.EMPTY):
                    break

            t1 = False
            for i in range(1, 8):
                if checkPosition(board, x - i, y + i, enemyColor):
                    t1 = True
                    attackPosition = [x - i, y + i]
                if checkPosition(board, x - i - 1, y + i + 1, Color.EMPTY) and t1:
                    attackArr.append(([x - i - 1, y + i + 1], attackPosition))
                if t1 and not checkPosition(board, x - i - 1, y + i + 1, Color.EMPTY):
                    break

            t1 = False
            for i in range(1, 8):
                if checkPosition(board, x - i, y - i, enemyColor):
                    t1 = True
                    attackPosition = [x - i, y - i]
                if checkPosition(board, x - i - 1, y - i - 1, Color.EMPTY) and t1:
                    attackArr.append(([x - i - 1, y - i - 1], attackPosition))
                if t1 and not checkPosition(board, x - i - 1, y - i - 1, Color.EMPTY):
                    break

            return attackArr

        moves = []

        if board.getColor(x, y) == Color.BLACK:
            moves = attackFigure(board, x, y, Color.WHITE)

        if board.getColor(x, y) == Color.WHITE:
            moves = attackFigure(board, x, y, Color.BLACK)

        if moves is None or len(moves) == 0:
            moves = nonAttackFigure(board, x, y)

        return moves


class Board:
    canvas = None
    defaultWidth = 1280
    defaultHeight = 720
    defaultBoardSize = (684, 684)
    defaultCountOfFigure = 12

    def __init__(self, backGroundName, width=defaultWidth, height=defaultHeight, boardSize=defaultBoardSize):
        self.canvas = Figure.canvas = tkinter.Canvas(width=width, height=height)
        self.canvas.pack()

        # startScreen
        self.startScreenArr = []
        for i in range(1, 9):
            img = Image.open(f'sprites/startGame/start{i}.png')
            img = img.resize((530, 180))
            self.startScreenArr.append(ImageTk.PhotoImage(img))

        self.startButton = 1
        self.t = None
        self.startFromFile = None
        self.exit = None
        pictureNumber = 0
        img = Image.open(f'sprites/startGame/startScreen.png')
        img = img.resize((width, height))
        imgTk = ImageTk.PhotoImage(img)
        img2 = Image.open('sprites/startGame/resumeGame.png')
        img2 = img2.resize((250, 100))
        imgTk2 = ImageTk.PhotoImage(img2)
        img3 = Image.open('sprites/startGame/exit.png')
        img3 = img3.resize((250, 100))
        imgTk3 = ImageTk.PhotoImage(img3)
        self.startScreen = self.canvas.create_image(width, height, image=imgTk, anchor='se')
        self.tk_id = self.canvas.create_image(370, 170, anchor='nw')
        self.fromfile = self.canvas.create_image(500, 351, anchor='nw')
        self.exitButton = self.canvas.create_image(500, 451, anchor='nw')
        self.canvas.bind('<ButtonPress-1>', self.klickToStart)
        self.canvas.bind('<Motion>', self.MotionStart)
        self.ArrOFFigurePosition = []
        try:
            while self.startButton is not None:
                if self.exit is not None:
                    self.canvas.itemconfig(self.exitButton, image=self.exit)
                    self.canvas.update()
                if self.exit is None:
                    self.canvas.itemconfig(self.exitButton, image=imgTk3)
                    self.canvas.update()
                if self.startFromFile is not None:
                    self.canvas.itemconfig(self.fromfile, image=self.startFromFile)
                    self.canvas.update()
                if self.startFromFile is None:
                    self.canvas.itemconfig(self.fromfile, image=imgTk2)
                    self.canvas.update()
                if self.t is not None:
                    self.canvas.itemconfig(self.tk_id, image=self.t)
                    self.canvas.update()
                if self.t is None:
                    self.canvas.itemconfig(self.tk_id, image=self.startScreenArr[pictureNumber])
                    pictureNumber = (pictureNumber + 1) % len(self.startScreenArr)
                    self.canvas.update()
                    self.canvas.after(200)
        except (tkinter.TclError):
            print('Game not start')
            return

        # background
        backG = Image.open(f'sprites/startGame/bakground.png')
        backG = backG.resize((width, height))
        backg = ImageTk.PhotoImage(backG)
        self.backGround = self.canvas.create_image(0, 0, image=backg, anchor='nw')
        img = Image.open(f'sprites/startGame/{backGroundName}')
        border = (((img.size[0] // 9) * boardSize[0]) // img.size[0],
                  ((img.size[1] // 9) * boardSize[1]) // img.size[1])
        gameZone = (boardSize[0] - border[0],
                    boardSize[1] - border[1])
        self.oneBlockSize = (gameZone[0] // 8, gameZone[1] // 8)
        img = img.resize(boardSize)
        boardimage = ImageTk.PhotoImage(img)
        boardToCenterX = (width - boardimage.width()) // 2
        boardToCenterY = (height - boardimage.height()) // 2
        self.gameZoneStart = (boardToCenterX + border[0] // 2, boardToCenterY + border[1] // 2)
        self.gameZoneEnd = (self.gameZoneStart[0] + gameZone[0], self.gameZoneStart[1] + gameZone[1])
        self.boardImg = self.canvas.create_image(boardToCenterX, boardToCenterY, image=boardimage, anchor='nw')

        # console
        self.board = []
        self.txtFile = 'Draughts.txt'

        self.gamers = Gamers()
        self.wichTurnTxt = self.canvas.create_image(self.gameZoneEnd[0] + 10, 0, anchor='nw')
        self.canvas.create_rectangle(10, 10, 250, 100, fill='light blue', outline='white', width=10)
        self.drawTxt = self.canvas.create_image(0, 0, anchor='nw')

        self.startGame(self.oneBlockSize, self.gameZoneStart)
        self.arrOfGreenBoards = []
        self.arrOfmoves = []

        # bind
        self.changePos = None
        self.canvas.bind('<ButtonPress-1>', self.mouseDown)
        self.canvas.bind('<B1-Motion>', self.mouseMove)
        self.canvas.bind('<ButtonRelease-1>', self.mouseUp)
        self.canvas.bind('<ButtonPress-3>', self.draw)

        tkinter.mainloop()

    def __repr__(self):
        repr = ''
        for row in range(8):
            for col in range(8):
                repr += str(self.board[row][col])
            repr += '\n'
        return repr

    def startGame(self, oneBlockSize, gameZoneStart):

        def createFigures(oneBlockSize, gameZoneStart ):

            for i, row in enumerate(self.ArrOFFigurePosition):
                oneRow = []
                if i == 8:
                    break
                for j, fig in enumerate(row[0]):
                    name = [i, j]
                    pozition = (gameZoneStart[0] + j * oneBlockSize[0],
                                    gameZoneStart[1] + i * oneBlockSize[1])
                    if fig == '.':
                        oneRow.append(Empty(name, oneBlockSize, pozition))
                    elif fig == '⛂':
                        oneRow.append(Draught(1, name, oneBlockSize, pozition))
                    elif fig == '⛀':
                        oneRow.append(Draught(2, name, oneBlockSize, pozition))
                    elif fig == '⛁':
                        oneRow.append(DraughtQuin(1, name, oneBlockSize, pozition))
                    elif fig == '⛃':
                        oneRow.append(DraughtQuin(2, name, oneBlockSize, pozition))
                self.board.append(oneRow)

        def writeToFile():
            with open(self.txtFile, 'w', encoding='UTF-8') as file:
                print("GAME START\n\n", file=file)
                print(self, file=file)

        def anotherThings():
            if self.ArrOFFigurePosition[8] == ['White Turn']:
                self.gamers.gamer1 = True
                self.gamers.gamer2 = False

            if self.ArrOFFigurePosition[8] == ['Black Turn']:
                self.gamers.gamer2 = True
                self.gamers.gamer1 = False

            # self.canvas.create_rectangle(0, 0, 250, 100, outline='white', width=10 )
            self.turn = self.gamers.turn()
            self.canvas.itemconfig(self.wichTurnTxt, image=self.turn)
            img = Image.open('sprites/draw/drawTXT1.png')
            img = img.resize((250, 170))
            self.drawimg = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.drawTxt, image=self.drawimg)

        newWrite = False
        if len(self.ArrOFFigurePosition) == 0:
            self.ArrOFFigurePosition = [['⛂.⛂.⛂.⛂.'],
                                           ['.⛂.⛂.⛂.⛂'],
                                           ['⛂.⛂.⛂.⛂.'],
                                           ['........'],
                                           ['........'],
                                           ['.⛀.⛀.⛀.⛀'],
                                           ['⛀.⛀.⛀.⛀.'],
                                           ['.⛀.⛀.⛀.⛀'], ['White Turn']]
            newWrite = True

        createFigures(oneBlockSize, gameZoneStart)
        if newWrite:
            writeToFile()
        elif not newWrite:
            text = f'\n\n{self.ArrOFFigurePosition[8][0]}\n{self}'
            self.writeToFile(text)
        anotherThings()

    def getColor(self, x, y):
        return self.board[x][y].color

    def getMoves(self, x, y):

        def checkMoves(x, y, color):
            attackArr = self.getAllAttackMovesForGamer(color)

            if attackArr == [] and self.getColor(x, y) == color:
                return self.board[x][y].getMoves(self, x, y)

            elif [x, y] in attackArr:
                return self.board[x][y].getMoves(self, x, y)

        if self.gamers.gamer1:
            print('white Turn')
            return checkMoves(x, y, Color.WHITE)

        if self.gamers.gamer2:
            print('black Turn')
            return checkMoves(x, y, Color.BLACK)

    def getAllAttackMovesForGamer(self, color):
        arr = []

        for row in range(8):
            for col in range(8):

                if self.board[row][col].color == color:
                    move = self.board[row][col].getMoves(self, row, col)

                    for i in move:
                        if i[1] is not None:
                            arr.append([row, col])

        return arr

    def move(self, xyFrom, xyTo, attackedPos):

        def tryDraw():
            if self.gamers.gamer1WantoDraw or self.gamers.gamer2WnatToDraw:
                self.gamers.swapturn()
                self.turn = self.gamers.turn()
                self.canvas.itemconfig(self.wichTurnTxt, image=self.turn)
                return True

        # move figure to new position
        def moveFigureToNewPosition():
            moveFrom = self.board[xyFrom[0]][xyFrom[1]]
            moveTo = self.board[xyTo[0]][xyTo[1]]
            print(f'{moveFrom.matrixPos} --> {moveTo.matrixPos}')

            if isinstance(self.board[xyFrom[0]][xyFrom[1]], DraughtQuin):
                self.board[xyTo[0]][xyTo[1]] = DraughtQuin(moveFrom.color, moveTo.matrixPos, moveFrom.size, moveTo.pozition)

            else:
                self.board[xyTo[0]][xyTo[1]] = Draught(moveFrom.color, moveTo.matrixPos, moveFrom.size, moveTo.pozition)

            self.board[xyFrom[0]][xyFrom[1]] = Empty(moveFrom.matrixPos, moveFrom.size, moveFrom.pozition)

        def tryAttacked():
            if attackedPos is not None:
                # delete attacked figure
                attackedFigure = self.board[attackedPos[0]][attackedPos[1]]
                self.board[attackedPos[0]][attackedPos[1]] = \
                    Empty(attackedFigure.matrixPos, attackedFigure.size, attackedFigure.pozition)

        def tryTransformFigure():
            changedFig = self.board[xyTo[0]][xyTo[1]]

            if xyTo[0] == 7 and changedFig.color == Color.BLACK:
                self.board[xyTo[0]][xyTo[1]] = DraughtQuin(1, changedFig.matrixPos, changedFig.size, changedFig.pozition)

            if xyTo[0] == 0 and changedFig.color == Color.WHITE:
                self.board[xyTo[0]][xyTo[1]] = DraughtQuin(2, changedFig.matrixPos, changedFig.size, changedFig.pozition)

        def tryEndGame():
            moveFrom = self.board[xyFrom[0]][xyFrom[1]]
            moveTo = self.board[xyTo[0]][xyTo[1]]
            turn = 'White Turn'
            if self.gamers.gamer2:
                turn = 'Black Turn'
            countFigureOnTable = self.countOfFiguresByType()
            text = f'\n\n{moveFrom.matrixPos} --> {moveTo.matrixPos}\n{countFigureOnTable}\n{turn}\n{self}'
            self.writeToFile(text)
            if countFigureOnTable[0] == 0 or countFigureOnTable[1] == 0:
                self.gameEnd()

            if countFigureOnTable[0] == 1 and countFigureOnTable[1] == 1:
                self.gameEnd()

        def tryAttackAgain():
            tryAttackAgain = self.board[xyTo[0]][xyTo[1]].getMoves(self, xyTo[0], xyTo[1])

            if tryAttackAgain and tryAttackAgain[0][1] is not None and attackedPos is not None:
                return

            self.gamers.swapturn()

        def whichTurn():
            self.turn = self.gamers.turn()
            self.canvas.itemconfig(self.wichTurnTxt, image=self.turn)

        if tryDraw():
            return

        moveFigureToNewPosition()
        tryAttacked()
        tryTransformFigure()
        tryEndGame()
        tryAttackAgain()
        whichTurn()

        print(self)

    def MotionStart(self, event):
        if 500 <= event.x <= 750 and 451 <= event.y <= 551:
            if self.exit is not None:
                return

            img = Image.open('sprites/startGame/exitWhite.png')
            img = img.resize ((250, 100))
            self.exit = ImageTk.PhotoImage(img)
            self.startFromFile = None
            self.t = None
            return

        if 500 <= event.x <= 750 and 350 <= event.y <= 450:
            if self.startFromFile is not None:
                return

            img = Image.open('sprites/startGame/resumeGameWhite.png')
            img = img.resize((250, 100))
            self.startFromFile = ImageTk.PhotoImage(img)
            self.t = None
            self.exit = None
            return

        if 370 <= event.x <= 900 and 170 <= event.y <= 350:
            if self.t is not None:
                return

            img = Image.open('sprites/startGame/startPresd.png')
            img = img.resize((530, 180))
            self.t = ImageTk.PhotoImage(img)
            self.startFromFile = None
            self.exit = None
            return

        self.t = None
        self.startFromFile = None
        self.exit = None

    def klickToStart(self, event):
        if self.t is None and self.startFromFile is None and self.exit is None:
            return

        if self.startFromFile is not None:
            with open('Draughts.txt', 'r', encoding='utf-8') as file:
                readedFile = file.read()
                readedFile = readedFile.replace('\n', '')
                if len(readedFile) < 74:
                    return

                oneRow = ''
                turn = ''
                count = 0
                for i in reversed(readedFile):
                    count +=1
                    if count == 75:
                        break
                    if count > 64:
                        turn += i
                    if count <= 64:
                        oneRow = i + oneRow
                        if len(oneRow) == 8:
                            self.ArrOFFigurePosition.insert(0, [oneRow])
                            oneRow = ''
                if turn == 'nruT etihW':
                    turn = 'Black Turn'
                if turn == 'nruT kcalB':
                    turn = 'White Turn'
                self.ArrOFFigurePosition.append([turn])

        if self.exit is not None:
            self.canvas.destroy()
            self.canvas.quit()
            return

        self.startButton = None
        self.canvas.delete(self.tk_id)
        self.canvas.delete(self.startScreen)
        self.canvas.delete(self.fromfile)
        self.canvas.delete(self.exitButton)
        self.canvas.unbind('<ButtonPress-1>')
        self.canvas.unbind('<Motion>')

    def mouseDown(self, event):
        for row in range(8):
            for col in range(8):
                self.startPoz = self.board[row][col].pozition
                self.startMatrix = self.board[row][col].matrixPos
                figure = self.board[row][col]
                if self.getColor(figure.matrixPos[0], figure.matrixPos[1]) != Color.EMPTY and figure.inside(event.x,
                                                                                                            event.y):
                    self.changePos = figure
                    self.dx, self.dy = event.x - figure.pozition[0], event.y - figure.pozition[1]
                    self.arrOfmoves = self.getMoves(self.startMatrix[0], self.startMatrix[1])
                    try:
                        for c, q in enumerate(self.arrOfmoves):
                            x, y = self.findBox(q[0])
                            x1, y1 = x + figure.size[0], y + figure.size[1]
                            self.arrOfGreenBoards.append(self.canvas.create_rectangle(x, y, x1, y1,
                                                                                      outline='green', width=5))
                    except TypeError:
                        pass
                    return
        self.changePos = None

    def mouseMove(self, event):
        if self.changePos is not None:
            self.changePos.move(event.x - self.dx, event.y - self.dy)

    def mouseUp(self, event):
        t = False
        try:
            for i in self.arrOfmoves:
                if self.board[i[0][0]][i[0][1]].inside(event.x, event.y):
                    self.changePos.move(self.startPoz[0], self.startPoz[1])
                    self.move(self.startMatrix, i[0], i[1])
                    t = True
                    break

        except (TypeError, AttributeError):
            pass
        if not t:
            try:
                self.changePos.move(self.startPoz[0], self.startPoz[1])
            except AttributeError:
                pass
        for i in self.arrOfGreenBoards:
            self.canvas.delete(i)
        self.changePos = None

    def draw(self, event):
        if 0 <= event.x <= self.gameZoneStart[0] and 0 <= event.y <= 200:
            if self.gamers.gamer1:
                self.gamers.gamer1WantoDraw = True

            if self.gamers.gamer2:
                self.gamers.gamer2WnatToDraw = True

            text = 'the player offers a draw'
            self.writeToFile(text)
            print(text)
            self.gamers.swapturn()
            self.turn = self.gamers.turn()
            self.canvas.itemconfig(self.wichTurnTxt, image=self.turn)

        if self.gamers.gamer1WantoDraw and self.gamers.gamer2WnatToDraw:
            text = 'draw'
            self.writeToFile(text)
            print(text)
            self.gameEnd()

    def findBox(self, xy):
        for row in self.board:
            for col in row:
                if col.matrixPos == xy:
                    return col.pozition

    def countOfFiguresByType(self):
        whiteFigures, blackFigures = 0, 0
        for row in range(8):
            for col in range(8):
                if self.getColor(row, col) == Color.BLACK:
                    blackFigures += 1
                if self.getColor(row, col) == Color.WHITE:
                    whiteFigures += 1
        return (whiteFigures, blackFigures)

    def writeToFile(self, text):
        with open(self.txtFile, 'a', encoding='UTF-8') as file:
            print(text, file=file)

    def gameEnd(self):

        def klick(event):
            if 500 <= event.x <= 750 and 280 <= event.y <= 380:
                self.canvas.destroy()
                self.canvas.quit()
                Board('board.png')
                return

            if 500 <= event.x <= 750 and 380 < event.y <= 480:
                self.canvas.destroy()
                self.canvas.quit()
                return

        def draw():
            arrOfTxt = []
            for i in range(1, 7):
                img = Image.open(f'sprites/draw/drawTXT{i}.png')
                img = img.resize((self.defaultWidth, self.defaultHeight))
                arrOfTxt.append(ImageTk.PhotoImage(img))

            img = Image.open('sprites/draw/draw.png')
            img = img.resize((self.defaultWidth, self.defaultHeight))
            imgtk = ImageTk.PhotoImage(img)
            drawpng = self.canvas.create_image(0, 0, image=imgtk, anchor='nw')
            drawtxt = self.canvas.create_image(0, 0, anchor='nw')
            pictureNumber = 0
            img2 = Image.open('sprites/startGame/newGame.png')
            img2 = img2.resize((250, 100))
            imgnewgame = ImageTk.PhotoImage(img2)
            imgRestartGame = self.canvas.create_image(500, 280, anchor='nw')
            img3 = Image.open('sprites/startGame/exit.png')
            img3 = img3.resize((250, 100))
            img3Tk = ImageTk.PhotoImage(img3)
            exit = self.canvas.create_image(500, 380, anchor='nw')
            try:
                while True:
                    self.canvas.itemconfig(exit, image=img3Tk)
                    self.canvas.update()
                    self.canvas.itemconfig(drawtxt, image=arrOfTxt[pictureNumber])
                    pictureNumber = (pictureNumber + 1) % len(arrOfTxt)
                    self.canvas.itemconfig(imgRestartGame, image=imgnewgame)
                    self.canvas.update()
                    self.canvas.update()
                    self.canvas.after(200)
            except (tkinter.TclError):
                pass

        def winnerOfGame(color):
            self.canvas.bind('<ButtonPress-1>', klick)

            if color == 'Noone':
                draw()
                return

            arrOfScreen = []
            for i in range(1, 5):
                img = Image.open(f'sprites/{color}Win/{color}Win{i}.png')
                img = img.resize((self.defaultWidth, self.defaultHeight))
                arrOfScreen.append(ImageTk.PhotoImage(img))

            arrOfTxt = []
            for i in range(1, 7):
                img = Image.open(f'sprites/{color}Win/{color}WinTXT{i}.png')
                img = img.resize((self.defaultWidth, self.defaultHeight))
                arrOfTxt.append(ImageTk.PhotoImage(img))

            arrOfPng = Figure.canvas = self.canvas.create_image(0, 0, anchor='nw')
            arrOftxt = Figure.canvas = self.canvas.create_image(0, 0, anchor='nw')
            pictureNumber1 = 0
            pictureNumber2 = 0
            img2 = Image.open('sprites/startGame/newGame.png')
            img2 = img2.resize((250, 100))
            imgnewgame = ImageTk.PhotoImage(img2)
            imgRestartGame = self.canvas.create_image(500, 280, anchor='nw')
            try:
                while True:
                    self.canvas.itemconfig(arrOfPng, image=arrOfScreen[pictureNumber1])
                    self.canvas.itemconfig(arrOftxt, image=arrOfTxt[pictureNumber2])
                    self.canvas.itemconfig(imgRestartGame, image=imgnewgame)
                    self.canvas.update()
                    pictureNumber1 = (pictureNumber1 + 1) % len(arrOfScreen)
                    pictureNumber2 = (pictureNumber2 + 1) % len(arrOfScreen)
                    self.canvas.update()
                    self.canvas.after(200)
            except (tkinter.TclError):
                    pass

        def delleteAllFigures():
            for row in range(7, -1, -1 ):
                for col in range(7, -1, -1):
                    del self.board[row][col]

        countOfFigure = self.countOfFiguresByType()
        winner = ''

        if countOfFigure[0] == 0:
            winner = 'black'

        if countOfFigure[1] == 0:
            winner = 'white'

        if countOfFigure[0] != 0 and countOfFigure[1] != 0:
            winner = 'Noone'

        text = f'The game winner is:{winner}'
        self.writeToFile(text)
        self.canvas.delete(self.wichTurnTxt)
        delleteAllFigures()
        self.canvas.delete(self.boardImg)
        self.canvas.delete(self.backGround)
        self.canvas.unbind('<ButtonPress-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.unbind('<ButtonPress-3>')
        winnerOfGame(winner)

class Program:
    def __init__(self):
        win = tkinter.Tk()
        win.title('Game Draughts')
        b = Board('board.png')

Program()

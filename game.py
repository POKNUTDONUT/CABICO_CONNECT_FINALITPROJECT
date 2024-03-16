# Import necessary libraries
import tkinter as tk  # Import the tkinter library and alias it as tk
from tkinter import *  # Import all classes and functions from tkinter module
from tkinter import messagebox  # Import the messagebox class from tkinter

# Function to handle selecting a column when a player clicks on it
def select(event):
    global canvas, board, plyr, p1, p2, gameText, newGameButton  # Global variables needed for manipulation
    row = 0  # Initialize row to 0
    col = -1  # Initialize col to -1
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8']  # Possible column numbers
    tags = canvas.gettags(CURRENT)  # Get the tags of the clicked item
    if not tags:  # If there are no tags (e.g., a colored piece), return
        return
    for s in tags:
        if s in nums:  # Check if the tag corresponds to a column number
            col = int(s)  # If so, set the column variable to that number
    # Find the lowest empty row in the selected column
    while row < 5:
        piece = board[row + 1][col]  # Get the piece in the row below the current row in the selected column
        cur_tags = canvas.gettags(piece)  # Get the tags of the piece
        if p1 not in cur_tags and p2 not in cur_tags:  # If the piece is empty
            row += 1  # Move to the next row
        else:
            break  # Otherwise, stop searching
    # Fill the lowest empty piece with the current player's color
    canvas.itemconfig(board[row][col], fill=plyr)  # Change the color of the piece to the current player's color
    canvas.itemconfig(board[row][col], tags=(plyr))  # Set the tag of the piece to the current player's color
    # Check for a win in different directions
    checkWin(row, col, vertical)  # Check for a win vertically
    if not gameOver:
        checkWin(row, col, horizontal)  # Check for a win horizontally
    if not gameOver:
        checkWin(row, col, downRight)  # Check for a win diagonally down-right
    if not gameOver:
        checkWin(row, col, upRight)  # Check for a win diagonally up-right
    # Check for a draw
    draw = True  # Assume draw initially
    for piece in board[0]:  # Iterate over the top row of the board
        cur_colors = canvas.gettags(piece)  # Get the tags of the piece
        if p1 not in cur_colors and p2 not in cur_colors:  # If the piece is empty
            draw = False  # Update draw status
            break
    # Update game status text
    if gameOver:  # If the game is over
        newText = plyr.upper() + " WINS!!!"  # Update game status text to show the winner
        updateLeaderboard(plyr)  # Update the leaderboard
        canvas.tag_bind("piece", '<Button-1>', '')  # Disable click event on pieces
        newGameButton.pack()  # Show the new game button
    elif draw:  # If the game is a draw
        newText = "DRAW"  # Update game status text to show a draw
        canvas.tag_bind("piece", '<Button-1>', '')  # Disable click event on pieces
        newGameButton.pack()  # Show the new game button
    else:  # If the game continues
        if plyr == p1:
            plyr = p2
        else:
            plyr = p1
        newText = plyr.upper() + "'s TURN"  # Update game status text to show the current player's turn
    canvas.itemconfig(gameText, fill=plyr, text=newText)  # Update the game status text

# Function to check for a win in a given direction
def checkWin(row, col, dir):
    global gameOver, board, canvas, plyr, winCoords  # Global variables needed for manipulation
    count = 0  # Counter for consecutive pieces of the same color
    startCoords = []  # Coordinates of the starting piece for the winning line
    endCoords = []  # Coordinates of the ending piece for the winning line
    ## Get coords of piece to start/end line
    ## start & end (x1+x2) / 2, (y1+y2) / 2
    # Iterate over pieces in the specified direction
    if dir == vertical:  # If checking vertically
        # Check vertically
        # Increment row to find the topmost piece in the column
        for i in range(5):
            if row < 5:
                row += 1
            else:
                break
        # Iterate over the column to check for a win
        for j in range(9):
            p = board[row][col]  # Get the current piece
            if plyr in canvas.gettags(p):  # If the piece belongs to the current player
                count += 1  # Increment the counter
                if count ==1:
                    startPoint = canvas.coords(p)  # Record the coordinates of the starting piece
                if count == 5:  # If there are 5 consecutive pieces of the same color
                    addLineCoords(startPoint, "start")  # Record the coordinates of the starting piece
                    addLineCoords(canvas.coords(p), "end")  # Record the coordinates of the ending piece
                    gameOver = True  # Set the game over flag
            else:
                count = 0  # Reset the counter
            if row - 1 >= 0:
                row -= 1  # Move to the next row
            else:
                break  # Stop searching if out of bounds
    # Horizontal
    elif dir == horizontal:  # If checking horizontally
        for i in range(5):
            if col < 5:
                col += 1
            else:
                break
        for j in range(9):
            p = board[row][col]
            if plyr in canvas.gettags(p):
                count += 1
                if count == 1:
                    startPoint = canvas.coords(p)
                if count == 5:
                    addLineCoords(startPoint, "start")
                    addLineCoords(canvas.coords(p), "end")
                    gameOver = True
            else:
                count = 0
            if col - 1 >= 0:
                col -= 1
            else:
                break
    # downRight
    elif dir == downRight:
        for i in range(5):
            if col < 8 and row < 5:
                col += 1
                row += 1
            else:
                break
        for k in range(9):
            p = board[row][col]
            if plyr in canvas.gettags(p):
                count += 1
                if count == 1:
                    startPoint = canvas.coords(p)
                if count == 5:
                    addLineCoords(startPoint, "start")
                    addLineCoords(canvas.coords(p), "end")
                    gameOver = True
            else:
                count = 0
            if col - 1 >= 0 and row - 1 >= 0:
                col -= 1
                row -= 1
            else:
                break
    # upRight
    elif dir == upRight:
        for i in range(5):
            if col > 0 and row < 5:
                col -= 1
                row += 1
            else:
                break
        for j in range(9):
            p = board[row][col]
            if plyr in canvas.gettags(p):
                count += 1
                if count == 1:
                    startPoint = canvas.coords(p)
                if count == 5:
                    addLineCoords(startPoint, "start")
                    addLineCoords(canvas.coords(p), "end")
                    gameOver = True
            else:
                count = 0
            if col + 1 <= 6 and row - 1 >= 0:
                col += 1
                row -= 1
            else:
                break
    if gameOver:  # If the game is over
        canvas.create_line(winCoords["x1"], winCoords["y1"], winCoords["x2"], winCoords["y2"], fill="#FCFCFC",
                           width="3p", arrow=tk.BOTH)  # Draw the winning line

def addLineCoords(coords, pos):
    global winCoords
    if pos == "start":
        winCoords["x1"] = (coords[0] + coords[2]) / 2
        winCoords["y1"] = (coords[1] + coords[3]) / 2
    elif pos == "end":
        winCoords["x2"] = (coords[0] + coords[2]) / 2
        winCoords["y2"] = (coords[1] + coords[3]) / 2

# Function to start a new game
def newGame():
    global canvas, newGameButton, colors, p1, p2
    colors = ["red", "yellow", "green", "blue", "gold"]  # Possible colors for players
    p1 = ''  # Initialize player 1's color
    p2 = ''  # Initialize player 2's color
    canvas.delete("all")  # Clear the canvas
    newGameButton.pack_forget()  # Hide the new game button
    showColorOptions("1")  # Show color options for player 1

# Function to set up the game board
def setupBoard():
    global gameOver, canvas, gameText, board, plyr
    # Draw the board
    canvas.delete(ALL)  # Clear the canvas
    board = []  # Initialize the game board
    gameText = ""  # Initialize the game text
    gameOver = False  # Initialize game over flag
    plyr = p1  # Set the current player to player 1

    # Calculate the starting position to center the board horizontally
    canvas_width = canvas.winfo_width()  # Get the width of the canvas
    board_width = 9 * 55  # Calculate the total width of the board (9 columns with a width of 55 each)
    colStart = (canvas_width - board_width) / 2  # Calculate the starting x-position for the first column

    rowStart = 50  # Set the starting y-position for the first row
    rowPos = rowStart  # Initialize the row position
    colPos = colStart  # Initialize the column position

    for x in range(6):
        new_list = []  # Initialize a new row list
        for y in range(9):
            # Create a new piece (circle) on the canvas and store its id
            spot = canvas.create_oval(colPos, rowPos, colPos + 45, rowPos + 45, fill="white", tags=("piece", y))
            colPos += 55  # Move to the next column position
            new_list.append(spot)  # Add the piece id to the current row list
        rowPos += 50  # Move to the next row position
        colPos = colStart  # Reset the column position for the next row
        board.append(new_list)  # Add the current row list to the game board

    canvas.tag_bind("piece", '<Button-1>', select)  # Bind the select function to the click event on pieces

    # Center the game text horizontally
    text_x = canvas_width / 2  # Calculate the x-coordinate for the game text
    gameText = canvas.create_text(text_x, rowPos + 65, fill=plyr, font='Arial 20 bold', text=plyr.upper() + "'s TURN")
    # Create the game text and center it horizontally

    canvas.pack()  # Pack the canvas into the tkinter window

# Dictionary to store wins for each color
color_wins = {"red": 0, "yellow": 0, "green": 0, "blue": 0, "gold": 0}

# Function to update the leaderboard when a player wins
def updateLeaderboard(color):
    color_wins[color] += 1  # Increment the win count for the specified color

# Function to display the leaderboard
def displayLeaderboard():
    leaderboard_text = "Leaderboard:\n"
    for color, wins in color_wins.items():
        leaderboard_text += f"{color.capitalize()}: {wins} wins\n"  # Add color and win count to the leaderboard text
    # Display leaderboard using a messagebox
    messagebox.showinfo("Leaderboard", leaderboard_text)  # Show the leaderboard in a messagebox

# Function to show the leaderboard
def showLeaderboard():
    displayLeaderboard()  # Call the displayLeaderboard function

# Function to reset the leaderboard
def resetLeaderboard():
    global color_wins  # Global variable needed for manipulation
    # Reset the wins for each color to 0
    color_wins = {"red": 0, "yellow": 0, "green": 0, "blue": 0, "gold": 0}
    messagebox.showinfo("Leaderboard Reset", "Leaderboard has been reset.")  # Show a message indicating leaderboard reset

# Function to handle picking player color
def pickColor(event):
    global p1, p2, gameText, colors  # Global variables needed for manipulation
    if p1 == '':  # If player 1's color is not chosen yet
        p1 = canvas.gettags(CURRENT)[0]  # Get the color tag of the clicked item as player 1's color
        colors.remove(p1)  # Remove player 1's color from the available colors
        canvas.delete(colors[-1])  # Delete the last color option (for player 2)
        canvas.delete(p1)  # Delete the selected color option (for player 1)
        showColorOptions("2")  # Show color options for player 2
    elif p2 == '':  # If player 2's color is not chosen yet
        p2 = canvas.gettags(CURRENT)[0]  # Get the color tag of the clicked item as player 2's color
        setupBoard()  # Set up the game board

# Function to display color options for players
def showColorOptions(p):
    global colors, gameText  # Global variables needed for manipulation
    if p == "1":  # If it's player 1's turn to choose color
        gameText = canvas.create_text(250, 300, font='Arial 20 bold', text="Choose your color" + "\nPlayer" + p, justify=CENTER)
    else:  # If it's player 2's turn to choose color
        canvas.itemconfig(gameText, text="Choose your color" + "\nPlayer" + p, justify=CENTER)
        # Update the game text to indicate player 2's turn to choose color
    startX = 120  # Starting x-coordinate for displaying color options
    startY = 150  # Starting y-coordinate for displaying color options
    for color in colors:  # Iterate over available colors
        option = canvas.create_oval(startX, startY, startX + 45, startY + 45, fill=color, tags=color)
        # Create a circular color option on the canvas
        canvas.tag_bind(color, '<Button-1>', pickColor)  # Bind the pickColor function to the click event on color options
        startX += 55  # Move to the next x-coordinate for the next color option

# Initialize Tkinter window
root = tk.Tk()  # Create the root window
root.title("CONNECT 5")  # Set the title of the window
root.geometry('550x550')  # Set the dimensions of the window

## Directions to check
vertical = 1  # Vertical direction
horizontal = 2  # Horizontal direction
downRight = 3  # Diagonal down-right direction
upRight = 4  # Diagonal up-right direction

## Coordinates for drawing the winning line
winCoords = {}  # Dictionary to store coordinates for drawing the winning line
gameOver = False  # Variable to track if the game is over
p1 = ''  # Variable to store player 1's color
p2 = ''  # Variable to store player 2's color
plyr = p1  # Variable to store the current player's color
board = []  # List to represent the game board
colors = []  # List to store available colors for players

# Create a canvas with the background image
canvas = tk.Canvas(root, width=500, height=500)  # Create a canvas widget
canvas.pack()  # Pack the canvas widget into the root window
gameText = canvas.create_text(280, 300, font='Arial 20 bold', text="Player 1 - Choose your color")  # Create game text
leaderboardButton = Button(root, text="Leaderboard", command=showLeaderboard)  # Create leaderboard button
newGameButton = Button(root, text="New Game", command=newGame)  # Create new game button
resetLeaderboardButton = Button(root, text="Reset Leaderboard", command=resetLeaderboard)  # Create reset leaderboard button
newGame()  # Start a new game
resetLeaderboardButton.pack(side="left",padx=(10, 5), pady=(10, 5))  # Pack reset leaderboard button
leaderboardButton.pack(side="right",padx=(5, 10), pady=(10, 5))  # Pack leaderboard button
root.mainloop()  # Start the Tkinter event loop

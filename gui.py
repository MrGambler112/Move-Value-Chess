
from data import STARTING_POSITION, PIECE_TEXT
from move_rules import is_legal_move
import tkinter as tk
from copy import deepcopy

# ─── Global Variables ──────────────────────────────────────────────
SQUARE_SIZE = 60
BOARD_OFFSET = 60
BOARD_SIZE = 8 * SQUARE_SIZE  # 480

white_time = 600  # seconds
black_time = 600
current_turn = "white"
timer_running = False
timer_job = None
game_board = None  # deepcopy of STARTING_POSITION during game

# ─── Window ────────────────────────────────────────────────────────
window = tk.Tk()
window.geometry("700x780")
window.title("Move Value Based Chess Engine")
window.resizable(False, False)
window.configure(bg="#2c2c2c")

# ─── Canvas ────────────────────────────────────────────────────────
canvas = tk.Canvas(window, width=600, height=540, bg="#2c2c2c", highlightthickness=0)
canvas.pack(pady=(60, 0))

# ─── Helper: Format Time ───────────────────────────────────────────
def fmt(secs):
    secs = int(secs)
    return f"{secs//60}:{secs%60:02d}"

# ─── Clear Canvas ──────────────────────────────────────────────────
def clear_canvas():
    canvas.delete("all")

# ─── Widget Tracking ────────────────────────────────────────────────
all_widgets = []  # all transient widgets (buttons, labels, frames, etc.)

def destroy_all_widgets():
    """Destroy every transient widget and clear the tracker."""
    for w in all_widgets:
        try:
            w.destroy()
        except tk.TclError:
            pass
    all_widgets.clear()
    # Also clean legacy game_widgets
    for w in game_widgets:
        try:
            w.destroy()
        except tk.TclError:
            pass
    game_widgets.clear()

def centered_btn(text, y, command, **kw):
    """Create a centered button with consistent styling."""
    defaults = dict(font=("Arial", 14, "bold"), bg="#4a4a4a", fg="white",
                    activebackground="#5a5a5a", bd=2, relief=tk.RAISED,
                    width=25, height=1)
    defaults.update(kw)
    btn = tk.Button(window, text=text, command=command, **defaults)
    btn.place(x=180, y=y)
    all_widgets.append(btn)
    return btn

# ═══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def show_main_menu():
    clear_canvas()
    destroy_all_widgets()
    global timer_running
    timer_running = False
    if timer_job:
        window.after_cancel(timer_job)

    # Decorative chessboard pattern in background
    for r in range(4):
        for c in range(4):
            x1 = 60 + c * 120
            y1 = 30 + r * 120
            x2 = x1 + 120
            y2 = y1 + 120
            colour = "#404040" if (r + c) % 2 == 0 else "#505050"
            canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="")

    canvas.create_text(300, 170, text="♚  CHESS  ♔",
                        font=("Arial", 36, "bold"), fill="#e0e0e0")
    canvas.create_text(300, 220, text="Move Value Engine",
                        font=("Arial", 16), fill="#aaaaaa")

    centered_btn("▶  Play Game  (10 min)", 300, lambda: start_game(600))
    centered_btn("⚙  Game Mode", 360, show_game_mode_menu)
    centered_btn("✕  Quit", 420, window.quit, bg="#6a3a3a", activebackground="#7a4a4a")

# ═══════════════════════════════════════════════════════════════════
#  GAME MODE MENU
# ═══════════════════════════════════════════════════════════════════

custom_time_entry = None
custom_time_label = None
custom_time_var = tk.StringVar(value="5")

def show_game_mode_menu():
    clear_canvas()
    destroy_all_widgets()

    canvas.create_text(300, 100, text="⚙  Game Mode",
                        font=("Arial", 30, "bold"), fill="#e0e0e0")

    centered_btn("Standard  (10 min)", 180, lambda: start_game(600))
    centered_btn("Bullet  (1 min)", 230, lambda: start_game(60))
    centered_btn("Blitz  (3 min)", 280, lambda: start_game(180))

    # Custom time
    lbl = tk.Label(window, text="Custom (minutes):", font=("Arial", 12),
                   bg="#2c2c2c", fg="#cccccc")
    lbl.place(x=200, y=340)
    all_widgets.append(lbl)

    entry = tk.Entry(window, textvariable=custom_time_var, font=("Arial", 12),
                     width=6, justify="center")
    entry.place(x=350, y=338)
    all_widgets.append(entry)
    custom_time_entry = entry

    centered_btn("Start Custom Game", 390, start_custom_game,
                 bg="#4a7a4a", activebackground="#5a8a5a")
    centered_btn("←  Back", 450, show_main_menu, bg="#3a3a3a")

def start_custom_game():
    try:
        mins = int(custom_time_var.get())
        if mins < 1:
            mins = 1
    except ValueError:
        mins = 5
    start_game(mins * 60)

# ═══════════════════════════════════════════════════════════════════
#  GAME SCREEN
# ═══════════════════════════════════════════════════════════════════

# Timer label references
white_timer_label = None
black_timer_label = None
turn_label = None
move_entry = None
game_widgets = []

def start_game(init_seconds):
    """Transition from menu to game screen with given time per player."""
    global white_time, black_time, current_turn, timer_running, timer_job, game_board
    white_time = init_seconds
    black_time = init_seconds
    current_turn = "white"
    timer_running = False
    if timer_job:
        window.after_cancel(timer_job)
        timer_job = None
    game_board = deepcopy(STARTING_POSITION)

    clear_canvas()
    destroy_all_widgets()

    # ── Timer bar ──
    bar = tk.Frame(window, bg="#1a1a1a", height=50)
    bar.place(x=0, y=5, width=700, height=50)
    bar.pack_propagate(False)

    wlbl = tk.Label(bar, text=f"White: {fmt(white_time)}",
                    font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    wlbl.pack(side=tk.LEFT, padx=(30, 0))

    tlbl = tk.Label(bar, text="White's turn", font=("Arial", 13),
                    bg="#1a1a1a", fg="#aaaaaa")
    tlbl.pack(side=tk.LEFT, expand=True)

    blbl = tk.Label(bar, text=f"Black: {fmt(black_time)}",
                    font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    blbl.pack(side=tk.RIGHT, padx=(0, 30))

    game_widgets.extend([bar, wlbl, tlbl, blbl])
    all_widgets.extend([bar, wlbl, tlbl, blbl])
    global white_timer_label, black_timer_label, turn_label
    white_timer_label = wlbl
    black_timer_label = blbl
    turn_label = tlbl

    # ── Draw board ──
    draw_board()

    # ── Bottom controls ──
    entry = tk.Entry(window, font=("Arial", 14), width=10, justify="center")
    entry.place(x=250, y=710)
    game_widgets.append(entry)
    all_widgets.append(entry)
    global move_entry
    move_entry = entry

    # Back to menu button
    bbtn = tk.Button(window, text="← Menu", font=("Arial", 10),
                     bg="#3a3a3a", fg="#aaaaaa", bd=0, command=show_main_menu)
    bbtn.place(x=10, y=710)
    game_widgets.append(bbtn)
    all_widgets.append(bbtn)

    entry.focus_set()

    # ── Timer management ──
    def update_timer():
        global white_time, black_time, timer_running, timer_job
        if not timer_running:
            return
        if current_turn == "white":
            white_time -= 1
            white_timer_label.config(text=f"White: {fmt(white_time)}")
            if white_time <= 0:
                white_time = 0
                white_timer_label.config(text="White: 0:00", fg="red")
                timer_running = False
                canvas.create_text(300, 270, text="⏰ Black Wins!\n(White ran out of time)",
                                   font=("Arial", 22, "bold"), fill="#ff4444", justify="center")
                return
        else:
            black_time -= 1
            black_timer_label.config(text=f"Black: {fmt(black_time)}")
            if black_time <= 0:
                black_time = 0
                black_timer_label.config(text="Black: 0:00", fg="red")
                timer_running = False
                canvas.create_text(300, 270, text="⏰ White Wins!\n(Black ran out of time)",
                                   font=("Arial", 22, "bold"), fill="#ff4444", justify="center")
                return
        timer_job = window.after(1000, update_timer)

    def start_timer():
        global timer_running
        if not timer_running:
            timer_running = True
            update_timer()

    def switch_turn():
        global current_turn
        current_turn = "black" if current_turn == "white" else "white"
        turn_label.config(text=f"{current_turn.capitalize()}'s turn")
        if current_turn == "white":
            white_timer_label.config(fg="#00cc44")
            black_timer_label.config(fg="white")
        else:
            black_timer_label.config(fg="#00cc44")
            white_timer_label.config(fg="white")

    window.start_timer = start_timer
    window.switch_turn = switch_turn

    # ── Submit move ──
    def submit_move_closure():
        global game_board
        raw = move_entry.get().strip().upper()
        if len(raw) != 4:
            move_entry.delete(0, tk.END)
            return
        cols = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        if raw[0] not in cols or raw[2] not in cols:
            move_entry.delete(0, tk.END)
            return
        try:
            sc = cols[raw[0]]
            sr = 8 - int(raw[1])
            ec = cols[raw[2]]
            er = 8 - int(raw[3])
        except (ValueError, IndexError):
            move_entry.delete(0, tk.END)
            return

        if sr < 0 or sr > 7 or er < 0 or er > 7:
            move_entry.delete(0, tk.END)
            return

        piece = game_board[sr][sc]
        if piece == "":
            move_entry.delete(0, tk.END)
            return
        # Check correct colour's turn
        if (current_turn == "white" and not piece.startswith("w")) or \
           (current_turn == "black" and not piece.startswith("b")):
            move_entry.delete(0, tk.END)
            return

        legal = is_legal_move(sr, sc, er, ec, game_board)
        if legal:
            game_board[er][ec] = game_board[sr][sc]
            game_board[sr][sc] = ""
            start_timer()
            switch_turn()
            draw_board()
        move_entry.delete(0, tk.END)

    window.submit_move = submit_move_closure

    # Move button (created AFTER submit_move_closure is defined)
    btn = tk.Button(window, text="Move", font=("Arial", 12, "bold"),
                    bg="#4a4a4a", fg="white", command=submit_move_closure)
    btn.place(x=350, y=707)
    game_widgets.append(btn)
    all_widgets.append(btn)

def draw_board():
    """Draw the board and pieces from game_board."""
    clear_canvas()
    board = game_board
    for row in range(8):
        for col in range(8):
            x1 = col * SQUARE_SIZE + BOARD_OFFSET
            y1 = row * SQUARE_SIZE + BOARD_OFFSET
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            colour = "#b58863" if (row + col) % 2 == 0 else "#f0d9b5"
            canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="")

    # Labels
    for row in range(8):
        yc = row * SQUARE_SIZE + BOARD_OFFSET + SQUARE_SIZE / 2
        canvas.create_text(40, yc, text=str(8 - row), fill="#e0e0e0", font=("Arial", 10))
        canvas.create_text(540, yc, text=str(8 - row), fill="#e0e0e0", font=("Arial", 10))
    for col in range(8):
        xc = col * SQUARE_SIZE + BOARD_OFFSET + SQUARE_SIZE / 2
        canvas.create_text(xc, 40, text=chr(65 + col), fill="#e0e0e0", font=("Arial", 10))
        canvas.create_text(xc, 540, text=chr(65 + col), fill="#e0e0e0", font=("Arial", 10))

    # Pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                xc = col * SQUARE_SIZE + BOARD_OFFSET + SQUARE_SIZE / 2
                yc = row * SQUARE_SIZE + BOARD_OFFSET + SQUARE_SIZE / 2
                colour = "black" if piece[0] == "b" else "white"
                canvas.create_text(xc, yc, text=PIECE_TEXT[piece],
                                   font=("Arial", 32), fill=colour)

show_main_menu()
window.mainloop()

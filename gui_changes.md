# GUI Redesign - chess.com Style Layout

## Changes made to `main.py` (June 10, 2026)

Converted the original yellow/white setup screen into a dark-themed chess.com-like layout.

---

## Window

| Setting | Old | New |
|---------|-----|-----|
| Size | 700x700 | 900x700 |
| Title | "Move Value Based Chess Engine" | "Move Value Chess" |
| Resizable | Yes | No |
| Background | white | `#302E2B` |

---

## Layout Diagram

```
900px
|-----------------------|
|  Black  10:00         |  <- Timer above board (centered)
|                       |
|  8x8 Chess Board     | Side Panel (250px, #262421)
|  (560x560)           | - Move Value Chess title
|  green + beige       | - Choose Colour [White][Black][Rand]
|                       | - AI Target Score [___]
|  Rank/file labels    | - [Start Game]
|  on left/top         | - Your Turn / Score / Captures
|                       | - Status text
|  White  10:00         | - [____] [Move] / [New Game]
|-----------------------|
```

---

## Board Colors

| Element | Color Code |
|---------|-----------|
| Light squares | `#EEEED2` |
| Dark squares | `#769656` |
| Square size | 70px |
| Piece font | Arial 34 |
| Board offset | X=45, Y=65 |

---

## Side Panel (x=630 to x=900)

### Pre-game widgets (setup_widgets):

| Widget | Text | Position |
|--------|------|----------|
| title_label | "Move Value\nChess" | x=645, y=25 |
| choose_color_label | "Choose Colour" | x=645, y=95 |
| white_color_button | "White" | x=645, y=125 |
| black_color_button | "Black" | x=718, y=125 |
| random_color_button | "Rand" | x=791, y=125 |
| target_label | "AI Target Score" | x=645, y=180 |
| score_entry | "10" (default) | x=675, y=205 |
| start_button | "Start Game" | x=660, y=250 |

### In-game widgets (game_widgets):

| Widget | Text | Position |
|--------|------|----------|
| turn_label | "Your Turn" / "AI Thinking..." | x=645, y=95 |
| score_label | "Player: X pts \| AI: Y pts \| Target: Z" | x=645, y=130 |
| player_captured_label | "Your captures: ..." | x=645, y=170 |
| ai_captured_label | "AI captures: ..." | x=645, y=195 |
| info_label | "Lifetime: W: X L: Y D: Z" | x=645, y=230 |
| status_label | Status messages | x=645, y=300 |
| move_entry | Move input (E2E4) | x=645, y=380 |
| move_button | "Move" | x=755, y=380 |
| new_game_button | "New Game" | x=665, y=450 |

### Timer labels (always visible):

| Widget | Text | Position |
|--------|------|----------|
| black_timer_label | "Black  mm:ss" | board_center - 80, y=12 |
| white_timer_label | "White  mm:ss" | board_center - 80, y=655 |

---

## Button Styling

### Green buttons (Start Game, Move):
- bg=`#81B64C`, fg=`#FFFFFF`
- activebackground=`#95C85A`
- relief="flat", cursor="hand2"

### Gray buttons (color picker, New Game, Exit):
- bg=`#525250`, fg=`#CFCFCF`
- activebackground=`#666666`, activeforeground=`#FFFFFF`
- relief="flat", cursor="hand2"

### Highlighted color button:
- bg=`#81B64C`, fg=`#FFFFFF`

---

## Timer Design

- Timers sit above (Black) and below (White) the board
- Active player's timer shows `#FFFFFF` text
- Inactive player's timer shows `#CFCFCF` text
- Bold 18pt font
- Panel background `#262421`

---

## New Functions Added

| Function | Line | Purpose |
|----------|------|---------|
| `select_white_color()` | 356 | Sets player to White, highlights button |
| `select_black_color()` | 366 | Sets player to Black, highlights button |
| `select_random_color()` | 376 | Random color, highlights button |
| `highlight_color_button()` | 386 | Styles a button as selected (green) |
| `unhighlight_color_button()` | 391 | Styles a button as unselected (gray) |
| `new_game()` | 397 | Resets board, returns to setup screen |
| `show_setup_widgets()` | 492 | Places all setup widgets in side panel |

---

## Existing Functions Updated

| Function | Changes |
|----------|---------|
| `draw_board()` | Uses `BOARD_DARK`/`BOARD_LIGHT` colors, muted rank/file labels |
| `draw_start_screen()` | Empty — no longer draws overlay (side panel replaces it) |
| `draw_everything()` | Draws dark side panel background on canvas |
| `refresh_display()` | Timer text shows "White mm:ss" / "Black mm:ss", active timer highlighted |
| `show_game_widgets()` | Places widgets in side panel area, timers above/below board |
| `show_game_over()` | Dark overlay on board area, no canvas rectangles, styled exit button |
| `start_game()` | Uses `selected_color` instead of hardcoded "white" |

---

## Color Constants

```
BACKGROUND         = "#302E2B"   # Window background
PANEL_BG           = "#262421"   # Side panel background
BOARD_LIGHT        = "#EEEED2"   # Light squares
BOARD_DARK         = "#769656"   # Dark squares
SELECTED_SQUARE    = "#F6F669"   # (reserved for click-to-move)
TEXT_COLOR         = "#FFFFFF"   # Primary text
MUTED_TEXT         = "#CFCFCF"   # Secondary/muted text
BUTTON_BG          = "#81B64C"   # Green buttons
BUTTON_HOVER       = "#95C85A"   # Button hover state
BUTTON_TEXT        = "#FFFFFF"   # Button text
```

---

## What Was Preserved

All game logic remains untouched:
- AI engine (`ai_engine.py`)
- Board logic (`board_logic.py`)
- Move rules (`move_rules.py`)
- Game state (`game_state.py`)
- Opening book (`bookmoves.py`)
- Data tables (`data.py`)

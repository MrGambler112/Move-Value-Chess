# Move Value Chess - Project Documentation

## Project Overview
A chess engine where the AI chooses moves based on computed "move values" rather than traditional minimax search. Built with Python and tkinter.

**Programmer:** Syed (Mahadi) Masuduzzaman

---

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | **GUI entry point** — tkinter window, board drawing, game loop, timer, player input |
| `data.py` | Starting board position, piece text symbols (unicode chess pieces), piece point values, position-value tables |
| `move_rules.py` | Movement rules for each piece type (pawn, rook, knight, bishop, queen, king) |
| `board_logic.py` | Board copy, king search, attack/check detection, checkmate/stalemate, legal move generation |
| `ai_engine.py` | AI move calculation: capture value, position value, development value, safety value, bias value, random tie-breaks |
| `bookmoves.py` | Opening book with 6 hardcoded openings (Italian, Sicilian, French, Caro-Kann, Queen's Gambit, King's Indian) |
| `game_state.py` | Capture tracking, score keeping, move history, lifetime stats, match saving to file |
| `Documentation/` | Existing docs (PDF flowchart + draft documentation) |
| `Mahadicodestyle/` | Code style analysis (identity card, fingerprint, style evolution, quick reference, DNA examples) |
| `toolstaughtinclass/` | Reference sheets (built-in functions, keywords, libraries, data structures, formatting, file I/O) |
| `Classresources/` | Course materials (SDLC, GUI programming, databases, project marking rubrics) |
| `chess_history.txt` | Saved match records |
| `chess_lifetime.txt` | Lifetime win/loss/draw stats |
| `README.txt` | Outdated — references `gui.py` which doesn't exist |

---

## GUI Location

- **File:** `main.py`
- **Library:** tkinter
- **Window:** 700x700, uses `canvas.create_rectangle`, `canvas.create_text`, tkinter Labels, Buttons, and Entry widgets
- **Layout:** Checkerboard drawn at offset (110, 110) with 60px squares. Labels for scores, timers, captures, status. Entry box for move input (format E2E4).
- **Game flow:** Setup screen → Start Game → Player enters moves → AI responds → Game over screen with results

---

## Architecture

### How the game runs:
1. `main.py` starts, draws the setup screen
2. Player sets AI target score, clicks "Start Game"
3. Game loop: player enters move → validated → executed → AI calculates best move → AI move executed
4. Timer runs (10 min per side), game ends on: checkmate, stalemate, target score reached, or timeout

### AI Move Value Formula:
```
Move Value = CaptureValue + PositionTableBonus + DevOrPositionValue - SafetyPenalty ± RandomTieBreak - BiasValue
```
- **CaptureValue:** Points of captured piece
- **PositionTableBonus:** Piece-square table difference (currently 0 — disabled)
- **DevelopmentValue:** Squares controlled by newly developed pieces
- **PositionValue:** Threats + protections - attackers (for already-developed pieces)
- **SafetyValue:** Penalty for exposing higher-value friendly pieces
- **RandomTieBreak:** ±0.01 to ±0.10 to vary equal moves
- **BiasValue:** Reduces value if player has a strong reply

### Project Status (from README):
**Done:** All legal positions for both colors

**Needs Implementation:**
- Timer (partially done in main.py)
- Point system (done — capture tracking works)
- Hardcoded chess openings (done — bookmoves.py)
- Position values, development values, safety values, move values (done in ai_engine.py)
- Random tie-break values (done)

---

## GUI Reference (main.py)

### Key GUI Components:
| Component | Type | Location (line) |
|-----------|------|-----------------|
| Window | tkinter.Tk | 24 |
| Canvas | tkinter.Canvas | 32-33 |
| White timer label | tkinter.Label | 797 |
| AI timer label | tkinter.Label | 800 |
| Turn label | tkinter.Label | 803 |
| Info label | tkinter.Label | 806 |
| Score label | tkinter.Label | 809 |
| Player captures | tkinter.Label | 812 |
| AI captures | tkinter.Label | 815 |
| Status label | tkinter.Label | 818 |
| Score entry | tkinter.Entry | 835-838 |
| Start button | tkinter.Button | 840-842 |
| Move entry | tkinter.Entry | 852 |
| Move button | tkinter.Button | 855 |
| Exit button | tkinter.Button | 858 |

### Key Functions:
| Function | Line | Purpose |
|----------|------|---------|
| `draw_board()` | 221 | Draws 8x8 checkerboard with labels |
| `draw_pieces()` | 251 | Draws pieces on board |
| `draw_start_screen()` | 264 | Draws setup panel |
| `submit_move()` | 692 | Handles player move input |
| `do_ai_turn()` | 612 | AI calculates and plays a move |
| `start_game()` | 652 | Initializes new game |
| `show_game_over()` | 458 | Displays endgame screen |
| `update_timers()` | 764 | Countdown timers per side |

---

## Code Style (Mahadi Signatures)
- `print ("text")` — space before `(`
- `== True` / `== False` always explicit
- Long `if/elif` chains instead of dictionaries
- `#lowercase section comments`
- Manual file open/close (no `with`)
- String concatenation with `+` (no `.join()`)
- `x = x + 1` instead of `x += 1`
- Sequential `if is_valid:` validation blocks

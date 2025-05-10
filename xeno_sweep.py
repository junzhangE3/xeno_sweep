import pygame
import random
import time
import os
import base64

# --- Configuration ---

# Pixel Art Colors (Same as before)
COLOR_BACKGROUND = (48, 32, 64)
COLOR_UI_BG_ACCENT = (72, 48, 96)
COLOR_GRID_LINES = (96, 64, 128)
COLOR_CELL_UNREVEALED = (60, 40, 80)
COLOR_CELL_REVEALED = (30, 20, 40)
COLOR_TEXT_BRIGHT = (255, 180, 90)
COLOR_TEXT_INSTRUCTIONS = (180, 220, 255)
COLOR_TEXT_ACCENT = (120, 220, 160)
COLOR_MINE_SHAPE = (240, 90, 120)
COLOR_FLAG_SHAPE = (255, 150, 60)
COLOR_CURSOR = (255, 255, 0)
COLOR_NUMBER_COLORS_PIXEL = {
    1: (100, 180, 255), 2: (100, 220, 100), 3: (255, 100, 100),
    4: (180, 100, 220), 5: (200, 50, 50),  6: (50, 200, 200),
    7: (100, 100, 100), 8: (200, 200, 200)
}
COLOR_BUTTON_PIXEL = (96, 64, 128)
COLOR_BUTTON_HOVER_PIXEL = (120, 80, 150)

# --- SCALED DIMENSIONS ---
# Grid Settings
GRID_ROWS = 10
GRID_COLS = 10
NUM_MINES = 15 # Can be adjusted if grid size changes significantly in cells
CELL_SIZE = 56 # Doubled from 28
GRID_MARGIN = 4  # Doubled from 2

# UI Layout
GAME_TITLE_AREA_HEIGHT = 60 # Doubled
HEADER_HEIGHT = 100        # Doubled

GRID_ACTUAL_WIDTH = GRID_COLS * (CELL_SIZE + GRID_MARGIN) + GRID_MARGIN
GRID_ACTUAL_HEIGHT = GRID_ROWS * (CELL_SIZE + GRID_MARGIN) + GRID_MARGIN

SCREEN_HEIGHT = GAME_TITLE_AREA_HEIGHT + HEADER_HEIGHT + GRID_ACTUAL_HEIGHT # Approx 764
SCREEN_WIDTH = int(SCREEN_HEIGHT * (16/9)) # Calculate width for 16:9, approx 1358

NPC_PANEL_WIDTH = SCREEN_WIDTH - GRID_ACTUAL_WIDTH # Approx 754

# Font paths
FONT_NAME_PIXEL = "PressStart2P-Regular.ttf"
FONT_SIZE_VSMALL = 12 # Was 6
FONT_SIZE_SMALL = 16  # Was 8
FONT_SIZE_MEDIUM = 20 # Was 10
FONT_SIZE_LARGE = 28  # Was 14
FONT_SIZE_TITLE = 32 # Was 18 (Adjusted for better title appearance)


ALIEN_ICON_FILENAME = "alien_head_icon.png"

# Game States
STATE_PLAYING = 0
STATE_GAME_OVER_WIN = 1
STATE_GAME_OVER_LOSE = 2


# --- Helper Classes ---
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.rect = pygame.Rect(
            NPC_PANEL_WIDTH + GRID_MARGIN + col * (CELL_SIZE + GRID_MARGIN),
            GAME_TITLE_AREA_HEIGHT + HEADER_HEIGHT + GRID_MARGIN + row * (CELL_SIZE + GRID_MARGIN),
            CELL_SIZE,
            CELL_SIZE
        )

    def draw(self, screen, font, is_selected, mine_sprite_img=None, flag_sprite_img=None):
        # ... (Cell drawing logic remains the same) ...
        if self.is_revealed:
            pygame.draw.rect(screen, COLOR_CELL_REVEALED, self.rect)
            if self.is_mine:
                if mine_sprite_img: # Placeholder for actual sprite loading
                    screen.blit(mine_sprite_img, self.rect.topleft)
                else:
                    pygame.draw.circle(screen, COLOR_MINE_SHAPE, self.rect.center, CELL_SIZE // 3)
            elif self.adjacent_mines > 0:
                num_color = COLOR_NUMBER_COLORS_PIXEL.get(self.adjacent_mines, COLOR_TEXT_BRIGHT)
                num_text = font.render(str(self.adjacent_mines), True, num_color)
                text_rect = num_text.get_rect(center=self.rect.center)
                screen.blit(num_text, text_rect)
        else:
            pygame.draw.rect(screen, COLOR_CELL_UNREVEALED, self.rect)
            if self.is_flagged:
                if flag_sprite_img: # Placeholder
                    screen.blit(flag_sprite_img, self.rect.topleft)
                else:
                    points = [
                        (self.rect.centerx, self.rect.top + CELL_SIZE * 0.15),
                        (self.rect.left + CELL_SIZE * 0.15, self.rect.centery + CELL_SIZE * 0.15),
                        (self.rect.right - CELL_SIZE * 0.15, self.rect.centery + CELL_SIZE * 0.15),
                    ]
                    pygame.draw.polygon(screen, COLOR_FLAG_SHAPE, points)

        pygame.draw.rect(screen, COLOR_GRID_LINES, self.rect, 1) # Border thickness might need scaling if desired

        if is_selected and game_state == STATE_PLAYING:
            pygame.draw.rect(screen, COLOR_CURSOR, self.rect, 3) # Scaled cursor thickness

class NPC:
    def __init__(self):
        base_y = GAME_TITLE_AREA_HEIGHT + HEADER_HEIGHT
        internal_padding = 20 # Scaled from 10

        self.portrait_rect = pygame.Rect(
            internal_padding,
            base_y + internal_padding,
            NPC_PANEL_WIDTH - 2 * internal_padding,
            160 # Doubled from 80
        )
        
        self.instruction_area_height = 120 # Doubled from 60
        self.instruction_rect = pygame.Rect(
            internal_padding,
            self.portrait_rect.bottom + internal_padding,
            NPC_PANEL_WIDTH - 2 * internal_padding,
            self.instruction_area_height
        )
        self.instructions = ["ARROWS: Move Cursor",
                             "ENTER: Scan Cell",
                             "SPACE: Place/Remove Beacon",
                             "R: Rescan Sector"]

        self.dialogue_rect = pygame.Rect(
            internal_padding,
            self.instruction_rect.bottom + internal_padding,
            NPC_PANEL_WIDTH - 2 * internal_padding,
            SCREEN_HEIGHT - self.instruction_rect.bottom - internal_padding - base_y
        )
        self.dialogue = ["Welcome Xeno-Miner!"]
        self.npc_portrait_img = None # Placeholder

    def set_dialogue(self, messages):
        self.dialogue = messages if isinstance(messages, list) else [messages]

    def draw(self, screen, font_v_sml, font_sml, font_med):
        # NPC Portrait (simple green rect)
        pygame.draw.rect(screen, (50, 150, 50), self.portrait_rect)
        npc_name_text = font_med.render("Zylar", True, COLOR_TEXT_BRIGHT)
        # Position name text within the scaled portrait rect
        screen.blit(npc_name_text, (self.portrait_rect.left + 10, self.portrait_rect.top + 10))

        # Instruction Area
        pygame.draw.rect(screen, COLOR_CELL_UNREVEALED, self.instruction_rect)
        pygame.draw.rect(screen, COLOR_GRID_LINES, self.instruction_rect, 2) # Scaled border
        inst_y_offset = self.instruction_rect.top + 10 # Scaled padding
        line_spacing_inst = font_v_sml.get_height() + 4 # Scaled spacing
        for line_text in self.instructions:
            text_surf = font_v_sml.render(line_text, True, COLOR_TEXT_INSTRUCTIONS)
            screen.blit(text_surf, (self.instruction_rect.left + 10, inst_y_offset))
            inst_y_offset += line_spacing_inst
            if inst_y_offset > self.instruction_rect.bottom - line_spacing_inst:
                break

        # Dialogue Area
        if self.dialogue:
            y_offset = self.dialogue_rect.top + 10
            max_chars_per_line = (self.dialogue_rect.width - 20) // (font_sml.size("X")[0] or 1)
            line_spacing_dialogue = font_sml.get_height() + 4

            for line_text in self.dialogue:
                words = line_text.split(' ')
                current_display_line = ""
                for word in words:
                    if len(current_display_line) + len(word) + 1 <= max_chars_per_line:
                        current_display_line += word + " "
                    else:
                        if current_display_line.strip():
                            text_surf = font_sml.render(current_display_line.strip(), True, COLOR_TEXT_BRIGHT)
                            screen.blit(text_surf, (self.dialogue_rect.left + 10, y_offset))
                            y_offset += line_spacing_dialogue
                        current_display_line = word + " "
                if current_display_line.strip():
                    text_surf = font_sml.render(current_display_line.strip(), True, COLOR_TEXT_BRIGHT)
                    screen.blit(text_surf, (self.dialogue_rect.left + 10, y_offset))
                    y_offset += line_spacing_dialogue
                if y_offset > self.dialogue_rect.bottom - line_spacing_dialogue:
                    break

# --- Game Logic Functions (create_grid, reveal_cell, check_win) ---
# These remain identical.
def create_grid():
    grid = [[Cell(r, c) for c in range(GRID_COLS)] for r in range(GRID_ROWS)]
    mines_placed = 0
    while mines_placed < NUM_MINES:
        r, c = random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)
        if not grid[r][c].is_mine:
            grid[r][c].is_mine = True
            mines_placed += 1
    for r_idx in range(GRID_ROWS):
        for c_idx in range(GRID_COLS):
            if grid[r_idx][c_idx].is_mine: continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r_idx + dr, c_idx + dc
                    if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and grid[nr][nc].is_mine:
                        count += 1
            grid[r_idx][c_idx].adjacent_mines = count
    return grid

def reveal_cell(grid, r_idx, c_idx, npc):
    if not (0 <= r_idx < GRID_ROWS and 0 <= c_idx < GRID_COLS): return 0
    cell_obj = grid[r_idx][c_idx]
    if cell_obj.is_revealed or cell_obj.is_flagged: return 0
    cell_obj.is_revealed = True
    if cell_obj.is_mine:
        npc.set_dialogue(["XENO-POD DETONATED!", "MISSION FAILURE!"])
        return -1
    revealed_count = 1
    if cell_obj.adjacent_mines == 0:
        if random.random() < 0.3: npc.set_dialogue(["Area clear.", "Scanning adjacent zones..."])
        else: npc.set_dialogue(["All clear here."])
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                revealed_count += reveal_cell(grid, r_idx + dr, c_idx + dc, npc)
    else:
        npc.set_dialogue([f"PROXIMITY: {cell_obj.adjacent_mines}", "Volatile pods nearby!"])
    return revealed_count

def check_win(grid_data):
    for r_cells in grid_data:
        for cell_obj in r_cells:
            if not cell_obj.is_mine and not cell_obj.is_revealed:
                return False
    return True

# --- Main Game ---
def main():
    global game_state

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Minesweeper")
    clock = pygame.time.Clock()
    
    try:
        font_v_sml = pygame.font.Font(FONT_NAME_PIXEL, FONT_SIZE_VSMALL)
        font_sml = pygame.font.Font(FONT_NAME_PIXEL, FONT_SIZE_SMALL)
        font_med = pygame.font.Font(FONT_NAME_PIXEL, FONT_SIZE_MEDIUM)
        font_lrg = pygame.font.Font(FONT_NAME_PIXEL, FONT_SIZE_LARGE)
        font_title = pygame.font.Font(FONT_NAME_PIXEL, FONT_SIZE_TITLE)
    except pygame.error:
        print(f"Warning: Pixel font '{FONT_NAME_PIXEL}' not found. Using default font.")
        # Fallback default font sizes (approx scaled)
        font_v_sml = pygame.font.Font(None, 20)
        font_sml = pygame.font.Font(None, 24)
        font_med = pygame.font.Font(None, 32)
        font_lrg = pygame.font.Font(None, 42)
        font_title = pygame.font.Font(None, 52)

    alien_mine_icon_img = None
    try:
        alien_mine_icon_img = pygame.image.load(ALIEN_ICON_FILENAME).convert_alpha()
        icon_base_size = HEADER_HEIGHT // 2 # Target half header height
        alien_mine_icon_img = pygame.transform.scale(alien_mine_icon_img, (icon_base_size, icon_base_size))
    except pygame.error:
        print(f"Warning: Alien icon '{ALIEN_ICON_FILENAME}' not found. Using placeholder.")

    grid = create_grid()
    npc = NPC()
    
    game_state = STATE_PLAYING
    start_time = time.time()
    elapsed_time = 0
    mines_remaining = NUM_MINES
    
    # Header elements positioning (scaled)
    header_padding = 30 # Scaled from 15
    
    # RESCAN Button
    button_width = 140 # Doubled
    button_height = HEADER_HEIGHT - (2 * 20) # Header height minus scaled top/bottom padding (was 10*2)
    reset_button_rect = pygame.Rect(
        SCREEN_WIDTH - button_width - header_padding,
        GAME_TITLE_AREA_HEIGHT + (HEADER_HEIGHT - button_height) // 2,
        button_width, button_height
    )
    
    mine_counter_x_start = NPC_PANEL_WIDTH + header_padding
    timer_x_center = NPC_PANEL_WIDTH + (GRID_ACTUAL_WIDTH // 2)


    cursor_row = 0
    cursor_col = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # ... (Event handling logic remains the same) ...
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_PLAYING:
                    if event.key == pygame.K_UP: cursor_row = max(0, cursor_row - 1)
                    elif event.key == pygame.K_DOWN: cursor_row = min(GRID_ROWS - 1, cursor_row + 1)
                    elif event.key == pygame.K_LEFT: cursor_col = max(0, cursor_col - 1)
                    elif event.key == pygame.K_RIGHT: cursor_col = min(GRID_COLS - 1, cursor_col + 1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        cell = grid[cursor_row][cursor_col]
                        if not cell.is_flagged and not cell.is_revealed:
                            result = reveal_cell(grid, cursor_row, cursor_col, npc)
                            if result == -1:
                                game_state = STATE_GAME_OVER_LOSE
                                for r_cells in grid:
                                    for c_obj in r_cells:
                                        if c_obj.is_mine: c_obj.is_revealed = True
                    elif event.key == pygame.K_SPACE:
                        cell = grid[cursor_row][cursor_col]
                        if not cell.is_revealed:
                            cell.is_flagged = not cell.is_flagged
                            if cell.is_flagged: mines_remaining -= 1; npc.set_dialogue(["BEACON PLACED."])
                            else: mines_remaining += 1; npc.set_dialogue(["BEACON REMOVED."])
                if event.key == pygame.K_r:
                    grid = create_grid(); npc.set_dialogue(["Sector re-scanned."]); game_state = STATE_PLAYING
                    start_time = time.time(); mines_remaining = NUM_MINES; cursor_row, cursor_col = 0, 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and reset_button_rect.collidepoint(mouse_pos):
                    grid = create_grid(); npc.set_dialogue(["Sector re-scanned."]); game_state = STATE_PLAYING
                    start_time = time.time(); mines_remaining = NUM_MINES; cursor_row, cursor_col = 0, 0
        
        if game_state == STATE_PLAYING and check_win(grid):
            game_state = STATE_GAME_OVER_WIN
            npc.set_dialogue(["ALL CLEAR!", "SECTOR SECURED!"])
            
        if game_state == STATE_PLAYING:
            elapsed_time = int(time.time() - start_time)
        
        screen.fill(COLOR_BACKGROUND)

        # Game Title Area
        pygame.draw.rect(screen, COLOR_BACKGROUND, (0, 0, SCREEN_WIDTH, GAME_TITLE_AREA_HEIGHT))
        game_title_text = font_title.render("ALIEN MINESWEEPER", True, COLOR_TEXT_BRIGHT)
        title_rect = game_title_text.get_rect(left=20, centery=GAME_TITLE_AREA_HEIGHT // 2) # Scaled padding
        screen.blit(game_title_text, title_rect)

        # Header Area
        header_y_start = GAME_TITLE_AREA_HEIGHT
        pygame.draw.rect(screen, COLOR_UI_BG_ACCENT, (0, header_y_start, SCREEN_WIDTH, HEADER_HEIGHT))
        
        current_x = mine_counter_x_start
        if alien_mine_icon_img:
            icon_y = header_y_start + (HEADER_HEIGHT - alien_mine_icon_img.get_height()) // 2
            screen.blit(alien_mine_icon_img, (current_x, icon_y))
            current_x += alien_mine_icon_img.get_width() + 10 # Scaled spacing
        else: # Placeholder
            pygame.draw.circle(screen, (50,200,50), (current_x + 20, header_y_start + HEADER_HEIGHT // 2), 20) # Scaled
            current_x += 50 # Scaled
        mine_text_val = f"{mines_remaining:03}"
        mine_text = font_med.render(mine_text_val, True, COLOR_TEXT_BRIGHT)
        screen.blit(mine_text, (current_x, header_y_start + (HEADER_HEIGHT - mine_text.get_height()) // 2))

        timer_val = f"{elapsed_time // 60:02}:{elapsed_time % 60:02}"
        time_text = font_med.render(timer_val, True, COLOR_TEXT_BRIGHT)
        time_text_rect = time_text.get_rect(centerx=timer_x_center,
                                            centery=header_y_start + HEADER_HEIGHT // 2)
        screen.blit(time_text, time_text_rect)

        btn_color = COLOR_BUTTON_HOVER_PIXEL if reset_button_rect.collidepoint(mouse_pos) else COLOR_BUTTON_PIXEL
        pygame.draw.rect(screen, btn_color, reset_button_rect)
        pygame.draw.rect(screen, COLOR_GRID_LINES, reset_button_rect, 2) # Scaled border
        reset_text_surf = font_sml.render("RESCAN", True, COLOR_TEXT_BRIGHT) # Using font_sml for button
        reset_text_rect_surf = reset_text_surf.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text_surf, reset_text_rect_surf)

        # NPC Panel Area
        npc_panel_y_start = GAME_TITLE_AREA_HEIGHT + HEADER_HEIGHT
        pygame.draw.rect(screen, COLOR_UI_BG_ACCENT, (0, npc_panel_y_start, NPC_PANEL_WIDTH, SCREEN_HEIGHT - npc_panel_y_start))
        npc.draw(screen, font_v_sml, font_sml, font_med)

        # Grid Area
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                is_selected = (r == cursor_row and c == cursor_col)
                grid[r][c].draw(screen, font_med, is_selected) # Using font_med for cell numbers
        
        # Game Over Messages
        msg_y_center = GAME_TITLE_AREA_HEIGHT + HEADER_HEIGHT + GRID_ACTUAL_HEIGHT // 2
        msg_x_center = NPC_PANEL_WIDTH + GRID_ACTUAL_WIDTH // 2

        if game_state == STATE_GAME_OVER_WIN:
            msg_surf = font_lrg.render("SECTOR CLEARED!", True, COLOR_TEXT_ACCENT)
            msg_rect = msg_surf.get_rect(center=(msg_x_center, msg_y_center))
            screen.blit(msg_surf, msg_rect)
        elif game_state == STATE_GAME_OVER_LOSE:
            msg_surf = font_lrg.render("PODS DETONATED!", True, COLOR_MINE_SHAPE)
            msg_rect = msg_surf.get_rect(center=(msg_x_center, msg_y_center))
            screen.blit(msg_surf, msg_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
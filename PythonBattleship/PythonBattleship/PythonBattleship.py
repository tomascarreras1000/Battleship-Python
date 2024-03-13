import sys
import msvcrt
import random

map_width = 10
map_height = 10
boat_list = []
ai_boat_list = []
shots = []
ai_shots = []
flags = []

show_cursor = True
def set_show_cursor(set_to):
    global show_cursor 
    show_cursor = set_to

winner = -1
def set_winner(set_to):
    global winner 
    winner = set_to

n_hits = 0
def hit():
    global n_hits
    n_hits += 1
    if (n_hits >= 21):
        set_winner(0)

n_ai_hits = 0
def ai_hit():
    global n_ai_hits
    n_ai_hits += 1
    if (n_ai_hits >= 21):
        set_winner(1)

class Placement:   
  
    def __init__(self, x_, y_, length_, is_vertical_):
        self.x = x_
        self.y = y_
        self.length = length_
        self.is_vertical = is_vertical_
        self.pending_placements = [5, 2, 2, 2, 3, 3, 4]
        self.iterator = self.pending_placements.index(length_)

    def set_x(self, x_):
        self.x = x_

    def set_y(self, y_):
        self.y = y_

    def set_length(self, length_):
        self.length = length_

    def set_is_vertical(self, is_vertical_):
        self.is_vertical = is_vertical_

    def set_iterator(self, iterator_):
        self.iterator = iterator_

    def set_placement(self, placement_):
        self.x = placement_.x
        self.y = placement_.y
        self.length = placement_.length
        self.is_vertical = placement_.is_vertical

class Boat:
    def __init__(self, placement_):
        if placement_.is_vertical:
            self.dict = {(placement_.y + value) * 10 + placement_.x: "O" for value in range(placement_.length) }
        else:
            self.dict = {placement_.y * 10 + placement_.x + value: "O" for value in range(placement_.length) }
        self.is_vertical = placement_.is_vertical

    def change_state(self, point_key, new_state):
        if point_key in self.dict.keys():
            self.dict[point_key] = new_state
class Pointer:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def set_x(self, x_):
        self.x = x_

    def set_y(self, y_):
        self.y = y_

class Cell:
    def __init__(self, dict_):
        self.dict = dict_

    def set_state(self, key_, state_):
        self.dict[key_] = state_

def main():
    try:
        print("Welcome to Battleship!")
        
        print_instructions()

        print("You can always press I to show the instructions again")

        while True:
            print("Press Enter to play")
            if "r" in str(msvcrt.getch()).lower():
                break

        run_game()

        print("Thanks for playing!")
        while True:
            print("Press Esc to exit")
            if "x" in str(msvcrt.getch()).lower():
                break

        exit_program()
                
    except Exception as e:
        print(f"An error occurred: {e}")
        exit_program()

def exit_program():
    print("Exiting the program...")
    sys.exit(0)


def print_instructions():
    print("- Move the cursor with WASD.\n- Use Enter/Return to confirm a boat placement and to shoot.\n- Use Q to switch from vertical to horizontal placement.\n- Use E to switch between boats.") #TODO

def run_game():
    
    is_game_setting = True
    placement = Placement(1, 1, 5, False)
    while is_game_setting:
        is_game_setting = setup_phase(placement)

    is_generating_ai_map = True
    ai_placement = Placement(1, 1, 5, False)
    while is_generating_ai_map:
        is_generating_ai_map = generate_ai_map(ai_placement)
    
    draw_ai_map() # TODO: take out

    is_game_running = True
    pointer = Pointer(1, 1)
    is_player_turn = True
    while is_game_running:

        if is_player_turn:
            is_player_turn = game_phase(pointer)
        else:
            is_player_turn = ai_game_phase()
        if winner != -1:
            break
        
    if winner == 1:
        print("You lose")
    elif winner == -1:
        print("Error")
    elif winner == 0:
        print("You win!")
        
def setup_phase(placement_):

    draw_map(placement_, True)

    input_char = str(msvcrt.getch()).lower()

    if "q" in input_char: 
        placement_.is_vertical = not placement_.is_vertical
        if placement_.is_vertical:
            if placement_.y + placement_.length > map_height:
                placement_.y = map_width - placement_.length + 1
        else:
            if placement_.x + placement_.length > map_width:
                placement_.x = map_width - placement_.length + 1

    elif "e" in input_char:
        cycle_placement(placement_)

    elif "w" in input_char: 
        if placement_.y > 1:
            placement_.y -= 1

    elif "a" in input_char: 
        if placement_.x > 1:
            placement_.x -= 1

    elif "s" in input_char: 
        if placement_.is_vertical:
            if placement_.y + placement_.length <= map_height:
                placement_.y += 1
        else:
            if placement_.y < map_height:
                placement_.y += 1

    elif "d" in input_char: 
        if placement_.is_vertical:
            if placement_.x < map_width:
                placement_.x += 1
        else:
            if placement_.x + placement_.length <= map_width:
                placement_.x += 1

    elif "i" in input_char:
        print_instructions()
    
    elif "r" in input_char: 
        if is_valid_placement(placement_):
            add_boat(placement_)
            if placement_.length == 0:
                return False
    return True

def generate_ai_map(placement_):
    
    # Select random cell and check if it's available
    new_placement = Placement(random.randint(1, 10), random.randint(1, 10), placement_.length, bool(random.getrandbits(1)))
    if is_valid_ai_placement(new_placement):
        placement_.set_placement(new_placement)
        add_ai_boat(placement_)
        if placement_.length == 0:
            return False

    return True


def game_phase(pointer_):
    
    draw_map(False, False)
    draw_enemy_map(pointer_)

    input_char = str(msvcrt.getch()).lower()

    if "f" in input_char:
        print(f"Flag at {pointer_.x, pointer_.y}")

    elif "w" in input_char: 
        if pointer_.y > 1:
            pointer_.y -= 1

    elif "a" in input_char: 
        if pointer_.x > 1:
            pointer_.x -= 1

    elif "s" in input_char: 
        if pointer_.y < map_height:
            pointer_.y += 1

    elif "d" in input_char: 
        if pointer_.x < map_width:
            pointer_.x += 1
    
    elif "i" in input_char:
        print_instructions()

    elif "r" in input_char: 
        return(shoot_at_pointer(pointer_))

    return True
    
def ai_game_phase():

    ret = True

    ai_shots_dict = {}
    for shot in ai_shots:
        ai_shots_dict = ai_shots_dict | shot.dict

    list = [k for k, v in ai_shots_dict.items() if v == "@"]

    is_random_shot = True
    new_pointer = Pointer(random.randint(1, 10), random.randint(1, 10))
    pointer_key = new_pointer.y * 10 + new_pointer.x

    if "@" in ai_shots_dict.values():
        pointer_key = list[random.randint(0, len(list) - 1)]
        if random.randint(0, 1):
            random_var = random.randint(-1, 1)
            if pointer_key % 10 <= 1 and random_var < 0 or pointer_key % 10 == map_width - 1 and random_var > 0:
                pass
            else:
                pointer_key += random_var

        else:
            random_var = random.randint(-1, 1) * 10
            if pointer_key // 10 <= 1 and random_var < 0 or pointer_key // 10 == map_width - 1 and random_var > 0:
                pass
            else:
                pointer_key += random_var

    if len(ai_shots) == 0 or not pointer_key in ai_shots_dict.keys():
        cell_state = "."
        for boat in boat_list:
            if pointer_key in boat.dict.keys():
                cell_state = "@"
                boat.change_state(pointer_key, cell_state)
                ai_hit()
                ret = False              

        cell = Cell({ pointer_key: cell_state })
        ai_shots.append(cell)        

        if cell_state == "@":
            for boat in boat_list:
                if pointer_key in boat.dict:

                    is_boat_destroyed = True
                    for value in boat.dict.values():
                        if not value == "@":
                            is_boat_destroyed = False
                            break
                    if is_boat_destroyed:

                        for key in boat.dict.keys():
                            for shot in ai_shots:
                                if key in shot.dict.keys():
                                    if boat.is_vertical:
                                        shot.set_state(key, "|")
                                    else:
                                        shot.set_state(key, "_")

    elif pointer_key in ai_shots_dict.keys():
        return False

    print("Shot at: ", pointer_key)

    return ret
       

def cycle_placement(placement_):

    it_ = placement_.iterator
    if it_ + 1 < len(placement_.pending_placements):
        it_ += 1
        while placement_.pending_placements[it_] == placement_.pending_placements[placement_.iterator]:
            if len(placement_.pending_placements) == 1:
                break # Just in case, we don't want infinite loops XD
            elif it_ + 1 < len(placement_.pending_placements):
                it_ += 1
            else:
                placement_.set_iterator(0)
        placement_.set_iterator(it_)
    else:
        placement_.set_iterator(0)
    placement_.set_x(1)
    placement_.set_y(1)
    placement_.set_length(placement_.pending_placements[placement_.iterator])
    placement_.set_is_vertical

def is_valid_placement(placement_):

    # Transform the placement into a dict
    placement_dict = {}
    if placement_.is_vertical:
        placement_dict = { (placement_.y + value) * 10 + placement_.x: "N" for value in range(placement_.length) }
    else:
        placement_dict = { placement_.y * 10 + placement_.x + value: "N" for value in range(placement_.length) }

    # Check it dict against the map dict
    map_dict = generate_map_dict(placement_, False)
    for key in placement_dict:
        if key in map_dict.keys():
            print("Invalid placement")
            return False

    return True

def is_valid_ai_placement(placement_):

    # Check boundaries first
    if placement_.is_vertical:
        if placement_.y + placement_.length > map_height:
            return False
    elif placement_.x + placement_.length > map_width:
        return False

    # Transform the placement into a dict
    placement_dict = {}
    if placement_.is_vertical:
        placement_dict = { (placement_.y + value) * 10 + placement_.x: "N" for value in range(placement_.length) } # TODO: Use the value for the boat's ID
    else:
        placement_dict = { placement_.y * 10 + placement_.x + value: "N" for value in range(placement_.length) }

    # Check it dict against the map dict
    map_dict = generate_ai_map_dict()
    for key in placement_dict:
        if key in map_dict.keys(): # The keys are the coords
            return False

    return True

def shoot_at_pointer(pointer_):

    ret = False

    pointer_key = pointer_.y * 10 + pointer_.x

    # Check if the point has been previously flagged
    if pointer_ in flags:
        flags.remove(pointer_)

    shots_dict = {}
    for shot in shots:
        shots_dict = shots_dict | shot.dict

    if len(shots) == 0 or not pointer_key in shots_dict.keys():
        cell_state = "."
        for boat in ai_boat_list:
            if pointer_key in boat.dict.keys():
                cell_state = "o"
                boat.change_state(pointer_key, cell_state)
                set_show_cursor(False)
                hit()
                ret = True

        cell = Cell({ pointer_key: cell_state })
        shots.append(cell)            

        if cell_state == "o":
            for boat in ai_boat_list:
                if pointer_key in boat.dict:

                    is_boat_destroyed = True
                    for value in boat.dict.values():
                        if not value == "o":
                            is_boat_destroyed = False
                            break
                    if is_boat_destroyed:

                        for key in boat.dict.keys():
                            for shot in shots:
                                if key in shot.dict.keys():
                                    if boat.is_vertical:
                                        shot.set_state(key, "|")
                                    else:
                                        shot.set_state(key, "_")

    return ret

def draw_map(placement_, has_placement):

    if has_placement:
        print(*fill_map_limits(generate_map_dict(placement_, has_placement)))
    else:
        print(*fill_map_limits(generate_map_dict(False, has_placement)))

def draw_enemy_map(pointer_):
    print(*fill_map_limits(generate_enemy_map_dict(pointer_)))

def draw_ai_map(): # Debugging only
    print(*fill_map_limits(generate_ai_map_dict()))

def generate_map_dict(placement_, has_placement):

    # Fill the map with the current boats first
    map_dict = {}
    for i in range(len(boat_list)):
        map_dict = map_dict | boat_list[i].dict
    
    # Fill the map with the ai shots after
    for j in range(len(ai_shots)):
        map_dict = map_dict | ai_shots[j].dict

    # Add the current placement on top
    if has_placement:
        placement_dict = {}
        if placement_.is_vertical:
            placement_dict = { (placement_.y + value) * 10 + placement_.x: "N" for value in range(placement_.length) }
        else:
            placement_dict = { placement_.y * 10 + placement_.x + value: "N" for value in range(placement_.length) }
        map_dict = map_dict | placement_dict
    return map_dict

def generate_ai_map_dict():

    # Fill the map with the current boats first
    map_dict = {}
    for i in range(len(ai_boat_list)):
        map_dict = map_dict | ai_boat_list[i].dict
    
    return map_dict

def generate_enemy_map_dict(pointer_):

    # Fill the map with the current boats first
    map_dict = {}  
    for shot in shots:
        map_dict = map_dict | shot.dict

    pointer_dict = {}
    if show_cursor:
        pointer_dict = { pointer_.y * 10 + pointer_.x: "X" }
    set_show_cursor(True)

    map_dict = map_dict | pointer_dict

    return map_dict

def fill_map_limits(map_dict_):

    map_list = [""]
    for y in range(map_height + 2):
        for x in range(map_width + 2):

            if x == map_width + 1:
                map_list.append("#\n")
            elif x == 0 or y == 0 or y == map_height + 1:
                map_list.append("#")
            elif y * 10 + x in map_dict_.keys():
                map_list.append(map_dict_[y * 10 + x])
            else:
                map_list.append(" ")
    return map_list

def add_boat(placement_):

    new_boat = Boat(placement_)
    boat_list.append(new_boat)
    placement_.pending_placements.remove(placement_.length)
    
    if len(placement_.pending_placements) == 0:
        placement_.set_length(0)
        return
    elif placement_.iterator > len(placement_.pending_placements) - 1:
        placement_.set_iterator(0)
    placement_.set_length(placement_.pending_placements[placement_.iterator])

def add_ai_boat(placement_):

    new_boat = Boat(placement_)
    ai_boat_list.append(new_boat)
    placement_.pending_placements.remove(placement_.length)
    
    if len(placement_.pending_placements) == 0:
        placement_.set_length(0)
        return
    elif placement_.iterator > len(placement_.pending_placements) - 1:
        placement_.set_iterator(0)
    placement_.set_length(placement_.pending_placements[placement_.iterator])

    # Start #
main()
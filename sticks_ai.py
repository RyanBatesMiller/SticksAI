
BUMP_MAP = {
    (0, 1): [],
    (0, 2): [(1, 1)],
    (0, 3): [(1, 2)],
    (0, 4): [(1, 3), (2, 2)],
    (1, 1): [(0, 2)],
    (1, 2): [(0, 3)],
    (1, 3): [(0, 4), (2, 2)],
    (1, 4): [(2, 3)],
    (2, 2): [(1, 3), (0, 4)],
    (2, 3): [(1, 4)],
    (2, 4): [(3, 3)],
    (3, 3): [(2, 4)],
    (3, 4): [],
    (4, 4): []
}


# ---------------------------
# STATE & RULES
# ---------------------------

def INITIAL_STATE():
    return ((1, 1), (1, 1))


def TERMINAL_STATE(state):
    return state[0] == (0, 0) or state[1] == (0, 0)


def WINNING_STATE(state):
    return state[0] != (0, 0) and state[1] == (0, 0)


def LOSING_STATE(state):
    return state[0] == (0, 0) and state[1] != (0, 0)


def CYCLE_DETECTOR(state, state_history, is_player_turn):
    return (state, is_player_turn) in state_history


# ---------------------------
# SUCCESSOR & ACTIONS
# ---------------------------

def NEXT_STATE(S, action):
    """Compute possible next states for an action."""
    (pL, pR), (oL, oR) = S
    moves = set()

    if action == "Attack Left":
        if pL > 0 and oL > 0:
            moves.add(((pL, pR), sorted_pair(oL + pL, oR)))
        if pR > 0 and oL > 0:
            moves.add(((pL, pR), sorted_pair(oL + pR, oR)))

    elif action == "Attack Right":
        if pL > 0 and oR > 0:
            moves.add(((pL, pR), sorted_pair(oL, oR + pL)))
        if pR > 0 and oR > 0:
            moves.add(((pL, pR), sorted_pair(oL, oR + pR)))

    elif action == "Bump":
        for newL, newR in BUMP_MAP.get(sorted_pair(pL, pR), []):
            moves.add(((newL, newR), (oL, oR)))

    return moves


def sorted_pair(a, b):
    """Helper to sum sticks & reset if needed."""
    return tuple(sorted(((0 if a >= 5 else a), (0 if b >= 5 else b))))


def SUCC_FN(S, is_player_turn):
    """Generate all legal successors from a state."""
    if not is_player_turn:
        S = swap_perspective(S)

    next_states = set()
    for action in ["Attack Left", "Attack Right", "Bump"]:
        next_states |= NEXT_STATE(S, action)

    return [swap_perspective(ns) if not is_player_turn else ns for ns in next_states]


def swap_perspective(S):
    """Swap player and opponent perspective."""
    return (S[1], S[0])


# ---------------------------
# EVALUATION & SEARCH
# ---------------------------

def EVAL(S):
    if WINNING_STATE(S):
        return 100
    if WINNING_STATE(swap_perspective(S)):
        return -100

    (pL, pR), (oL, oR) = S
    player_alive = (pL > 0 or pR > 0)

    player_score = pL + pR
    opponent_score = oL + oR

    # Encourage staying alive and winning
    survival_bonus = 0
    if player_alive:
        survival_bonus += 50

    return (player_score - opponent_score) + survival_bonus


def MINIMAX_ALPHA_BETA(S, depth, is_maximizing, alpha, beta):
    if TERMINAL_STATE(S) or depth == 0:
        return EVAL(S), None

    if is_maximizing:
        max_eval = float('-inf')
        best_move = None
        for child in SUCC_FN(S, True):
            eval_score, _ = MINIMAX_ALPHA_BETA(child, depth - 1, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = child
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for child in SUCC_FN(S, False):
            eval_score, _ = MINIMAX_ALPHA_BETA(child, depth - 1, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = child
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


# ---------------------------
# USER INTERACTION
# ---------------------------

def get_user_move(state, user_first):
    """Ask user for move and apply it."""
    swapped = not user_first
    if swapped:
        state = swap_perspective(state)

    while True:
        print("\nYour turn! Choose a move:")
        print("1: Attack Left")
        print("2: Attack Right")
        print("3: Bump")

        try:
            choice = int(input("Enter move (1-3): "))
            if choice not in [1, 2, 3]:
                raise ValueError("Choose 1, 2, or 3.")

            move = {1: "Attack Left", 2: "Attack Right", 3: "Bump"}[choice]
            options = list(NEXT_STATE(state, move))

            if not options:
                print("Invalid move. Try again.")
                continue

            if len(options) > 1:
                print("\nSelect an option:")
                for idx, opt in enumerate(options):
                    display = opt if not swapped else swap_perspective(opt)
                    print(f"{idx + 1}: {display}")
                while True:
                    sel = int(input("Choose an option: ")) - 1
                    if 0 <= sel < len(options):
                        state = options[sel]
                        break
                    print("Invalid option.")
            else:
                state = options[0]

            if swapped:
                state = swap_perspective(state)

            return state

        except ValueError:
            print("Invalid input. Try again.")


def choose_difficulty():
    difficulty_map = {
        "beginner": 2, "rookie": 5, "intermediate": 10, "pro": 15
    }
    while True:
        diff = input("Choose difficulty (beginner, rookie, intermediate, pro): ").lower()
        if diff in difficulty_map:
            return difficulty_map[diff]
        print("Invalid choice. Try again.")


# ---------------------------
# GAME LOOP
# ---------------------------

def PLAY_INTERACTIVE():
    print("Welcome to Sticks!")
    user_first = input("Do you want to go first? (y/n): ").lower() == 'y'
    depth = choose_difficulty()

    state = INITIAL_STATE()
    is_player_turn = user_first
    state_history = {(state, is_player_turn)}

    while not TERMINAL_STATE(state):
        print(f"\nCurrent state: {state}")
        if is_player_turn:
            state = get_user_move(state, user_first)
        else:
            print("AI is thinking...")
            _, state = MINIMAX_ALPHA_BETA(state, depth, True, float('-inf'), float('inf'))
            print(f"AI chose: {state}")

        is_player_turn = not is_player_turn
        if CYCLE_DETECTOR(state, state_history, is_player_turn):
            print("\nDraw! The game has entered a cycle.")
            return
        state_history.add((state, is_player_turn))

    print(f"\nGame Over! Final State: {state}")
    if (WINNING_STATE(state) and user_first) or (LOSING_STATE(state) and not user_first):
        print("You win!")
    else:
        print("AI wins!")

def PLAY_SELF(depth):
    """Simulates a game where the AI plays against itself using alpha-beta pruning."""
    state = INITIAL_STATE()
    is_player_turn = True  # Player 1 starts
    state_history = {(state, is_player_turn)}

    while not TERMINAL_STATE(state):
        print(f"{state}... Player 1 turn..." if is_player_turn else f"{state}... Player 2 turn...")

        _, state = MINIMAX_ALPHA_BETA(state, depth, is_player_turn, float('-inf'), float('inf'))

        is_player_turn = not is_player_turn
        if CYCLE_DETECTOR(state, state_history, is_player_turn):
            print("Draw! The game has entered a cycle.")
            return

        state_history.add((state, is_player_turn))

    print(f"\nGame Over! Final State: {state}")
    if WINNING_STATE(state):
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")



# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":
    mode = input("Play interactive (i) or self-play AI vs. AI (s)? ").lower()
    if mode == 'i':
        PLAY_INTERACTIVE()
    elif mode == 's':
        depth = choose_difficulty()
        PLAY_SELF(depth)
    else:
        print("Invalid choice.")

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

def NEXT_STATE(S, A):
    (pL, pR), (oL, oR) = S
    moves = set()

    if A == "Attack Left":
        if pL > 0 and oL > 0:
            moves.add(((pL, pR), tuple(sorted((oL + pL if oL + pL < 5 else 0, oR)))))
        if pR > 0 and oL > 0:
            moves.add(((pL, pR), tuple(sorted((oL + pR if oL + pR < 5 else 0, oR)))))
    elif A == "Attack Right":
        if pL > 0 and oR > 0:
            moves.add(((pL, pR), tuple(sorted((oL, oR + pL if oR + pL < 5 else 0)))))
        if pR > 0 and oR > 0:
            moves.add(((pL, pR), tuple(sorted((oL, oR + pR if oR + pR < 5 else 0)))))
    elif A == "Bump":
        bumped_player_hands = BUMP_MAP.get(tuple(sorted((pL, pR))), [])
        moves = {((newL, newR), (oL, oR)) for (newL, newR) in bumped_player_hands}

    return moves

def SUCC_FN(S, is_player_turn):
    if not is_player_turn:
        S = (S[1], S[0])
    legal_successive_states = []
    next_states = set()
    for move in ["Attack Left", "Attack Right", "Bump"]:
        next_states |= NEXT_STATE(S, move)
    for new_state in next_states:
        if not is_player_turn:
            new_state = (new_state[1], new_state[0])
        legal_successive_states.append(new_state)
    return legal_successive_states

def EVAL(S):
    if WINNING_STATE(S):
        return 100
    if WINNING_STATE((S[1], S[0])):
        return -100
    (pL, pR), (oL, oR) = S
    return pL + pR - (oL + oR)

def MINIMAX_ALPHA_BETA(S, depth, is_maximizing, alpha, beta):
    if TERMINAL_STATE(S) or depth == 0:
        return EVAL(S), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for next_state in SUCC_FN(S, True):
            eval_score, _ = MINIMAX_ALPHA_BETA(next_state, depth - 1, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = next_state
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for next_state in SUCC_FN(S, False):
            eval_score, _ = MINIMAX_ALPHA_BETA(next_state, depth - 1, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = next_state
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_user_move(state, user_first):
    is_swapped = not user_first
    if is_swapped:
        state = (state[1], state[0])

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
            next_states = list(NEXT_STATE(state, move))
            if not next_states:
                print("Invalid move, try again.")
                continue
            if len(next_states) > 1:
                print("\nSelect a bump option:")
                for i, option in enumerate(next_states):
                    display = option if not is_swapped else (option[1], option[0])
                    print(f"{i+1}: {display}")
                while True:
                    idx = int(input("Choose an option: ")) - 1
                    if 0 <= idx < len(next_states):
                        state = next_states[idx]
                        break
                    print("Invalid option, try again.")
            else:
                state = next_states[0]
            if is_swapped:
                state = (state[1], state[0])
            return state
        except ValueError as e:
            print(e)

def PLAY_INTERACTIVE():
    print("Welcome to Sticks!")
    user_first = input("Do you want to go first? (y/n): ").lower() == 'y'
    difficulty_map = {
        "beginner": 2, "rookie": 5, "intermediate": 10,
        "pro": 15, "all-star": 20, "genius": 25
    }
    while True:
        diff = input("Choose difficulty (beginner, rookie, intermediate, pro, all-star, genius): ").lower()
        if diff in difficulty_map:
            depth = difficulty_map[diff]
            break
        print("Invalid choice.")

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
    if WINNING_STATE(state) and user_first or LOSING_STATE(state) and not user_first:
        print("You win!")
    else:
        print("AI wins!")

if __name__ == "__main__":
    PLAY_INTERACTIVE()

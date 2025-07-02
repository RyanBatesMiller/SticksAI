# SticksAI

This is an implementation of the classic hand game **Sticks** (also known as Chopsticks) with an **AI opponent** that uses **Minimax with Alpha-Beta pruning**.

## 📜 Rules

- Each player has two hands.
- Each hand starts with 1 stick.
- On your turn, you can:
  - **Attack Left**: Tap the opponent’s left or right hand with your left or right hand, adding your sticks to theirs.
  - **Attack Right**: Same as above, but targeting the opposite hand.
  - **Bump**: Redistribute your sticks between your own hands according to legal bump rules.
- If any hand reaches 5 sticks, it is reset to 0.
- If both hands are 0, that player loses.

## 🤖 Features

- Human vs AI gameplay.
- AI vs AI gameplay.
- User chooses who goes first.
- Multiple difficulty levels:
  - **beginner**: depth 2
  - **rookie**: depth 5
  - **intermediate**: depth 10
  - **pro**: depth 15
- Cycle detection — prevents infinite loops by declaring a draw if a state repeats.

## 🚀 How to Run

```bash
python sticks_game.py
```
📌 How to Play

1. Choose whether to go first or second.
2. Choose your difficulty.
3. On your turn, pick Attack Left, Attack Right, or Bump.
*If your bump move has multiple results, you can choose the configuration.*

📂 File Structure

- sticks_ai.py — The main game logic.
- README.md — This file.
  
✅ Example
```bash
Do you want to go first? (y/n): y
Choose difficulty (beginner, rookie, intermediate, pro): intermediate

Current state: ((1, 1), (1, 1))

Your turn! Choose a move:
1: Attack Left
2: Attack Right
3: Bump
Enter move (1-3): 1

AI is thinking...
AI chose: ((0, 2), (1, 1))
```
...
✍️ Author
Ryan Miller

import random
import os
import platform

# 清除畫面 — 支援 Windows / Mac / Linux
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# 撲克牌資料
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

rank_value = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13, "A": 1
}

def create_deck():
    deck = [(r, s) for s in suits for r in ranks]
    random.shuffle(deck)
    return deck

def hand_string(hand):
    return "  ".join([f"{i+1}:{r}{s}" for i, (r, s) in enumerate(hand)])

def pick_card_hidden(player_num, hand):
    clear()
    print(f"====== 玩家{player_num} 請看你的手牌（不要讓對方看到） ======\n")
    print(hand_string(hand))
    choice = input(f"\n玩家{player_num}，請選擇要出的牌編號（1-5）： ")

    while not choice.isdigit() or not (1 <= int(choice) <= len(hand)):
        choice = input("編號錯誤，請重新輸入（1-5）： ")

    picked = hand.pop(int(choice) - 1)
    clear()  # 出牌後立即隱藏
    return picked

def draw_card_if_needed(hand, deck):
    while len(hand) < 5 and deck:
        hand.append(deck.pop())


# ===== 遊戲開始 =====
deck = create_deck()

player1_hp = 25
player2_hp = 25

player1 = [deck.pop() for _ in range(5)]
player2 = [deck.pop() for _ in range(5)]

round_num = 1

print("===== 撲克牌對戰遊戲開始（玩家vs.玩家）！ =====")
input("按 Enter 開始...")

while player1_hp > 0 and player2_hp > 0 and (player1 or player2):

    print(f"\n===== 第 {round_num} 回合 =====")
    print(f"玩家1 HP：{player1_hp}")
    print(f"玩家2 HP：{player2_hp}")
    print(f"牌庫剩餘：{len(deck)}")

    # 玩家1選牌
    input("\n請玩家1準備，按 Enter 查看手牌...")
    card1 = pick_card_hidden(1, player1)

    # 玩家2選牌
    input("請玩家2準備，按 Enter 查看手牌...")
    card2 = pick_card_hidden(2, player2)

    r1, s1 = card1
    r2, s2 = card2
    v1 = rank_value[r1]
    v2 = rank_value[r2]

    print("\n===== 回合結果 =====")
    print(f"玩家1 出牌：{r1}{s1}")
    print(f"玩家2 出牌：{r2}{s2}")

    # ===== 回血 =====
    if s1 == "♥":
        player1_hp += v1
        print(f"玩家1 使用紅心回血 +{v1} → HP: {player1_hp}")

    if s2 == "♥":
        player2_hp += v2
        print(f"玩家2 使用紅心回血 +{v2} → HP: {player2_hp}")

    # ===== 反擊 =====
    if s1 == "♦" and s2 in ["♠", "♣"]:
        player2_hp -= v2
        print(f"玩家1 方塊反擊 → 玩家2 -{v2} → {player2_hp}")

    if s2 == "♦" and s1 in ["♠", "♣"]:
        player1_hp -= v1
        print(f"玩家2 方塊反擊 → 玩家1 -{v1} → {player1_hp}")

    # ===== 正常攻擊 =====
    if s1 in ["♠", "♣"] and s2 != "♦":
        player2_hp -= v1
        print(f"玩家1 攻擊 → 玩家2 -{v1} → {player2_hp}")

    if s2 in ["♠", "♣"] and s1 != "♦":
        player1_hp -= v2
        print(f"玩家2 攻擊 → 玩家1 -{v2} → {player1_hp}")

    # ===== 出牌後補牌（P1 & P2）=====
    draw_card_if_needed(player1, deck)
    draw_card_if_needed(player2, deck)
    input("\n按 Enter 進入下一回合...")
    round_num += 1
    clear()

# ===== 遊戲結果 =====
print("\n===== 遊戲結束 =====")
if player1_hp <= 0 and player2_hp <= 0:
    print("平手！兩人同時倒下")
elif player1_hp <= 0:
    print("玩家2 勝利！")
elif player2_hp <= 0:
    print("玩家1 勝利！")
else:
    if player1_hp > player2_hp:
        print("牌用完，玩家1 HP 較高 → 玩家1勝利")
    elif player2_hp > player1_hp:
        print("牌用完，玩家2 HP 較高 → 玩家2勝利")
    else:
        print("牌用完，HP相同 → 平手")

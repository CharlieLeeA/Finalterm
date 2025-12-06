# ============================================
# final_term3.py - 撲克牌對戰遊戲主程式
# 整合版：可選擇 玩家vs電腦 或 玩家vs玩家 模式
# ============================================

import random
import os
import platform

# ===== 清除畫面函數 =====
def clear():
    """清除終端機畫面，支援 Windows / Mac / Linux"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# ===== 撲克牌基本資料 =====
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

rank_value = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13, "A": 1
}

def create_deck():
    """建立並洗牌一副52張撲克牌"""
    deck = [(r, s) for s in suits for r in ranks]
    random.shuffle(deck)
    return deck

def hand_string(hand):
    """將手牌轉換成顯示字串，格式：編號:點數花色"""
    return "  ".join([f"{i+1}:{r}{s}" for i, (r, s) in enumerate(hand)])

def draw_card_if_needed(hand, deck):
    """補牌：當手牌少於5張時，從牌庫抽牌補滿"""
    while len(hand) < 5 and deck:
        hand.append(deck.pop())

# ===== 玩家 vs 電腦 模式的函數 =====
def player_pick_card(hand):
    """玩家選擇要出的牌"""
    print("\n你的手牌：")
    print(hand_string(hand))
    choice = input("\n請選擇要出的牌編號（1-5）： ")

    while not choice.isdigit() or not (1 <= int(choice) <= len(hand)):
        choice = input("編號錯誤，請重新輸入（1-5）： ")

    return hand.pop(int(choice) - 1)

def computer_pick_card(computer_hand, player_hp, computer_hp):
    """電腦 AI 選牌邏輯"""
    hearts = [(i, c) for i, c in enumerate(computer_hand) if c[1] == "♥"]
    attacks = [(i, c) for i, c in enumerate(computer_hand) if c[1] in ["♠", "♣"]]
    diamonds = [(i, c) for i, c in enumerate(computer_hand) if c[1] == "♦"]
    
    # 血量低時優先回血
    if computer_hp <= 10 and hearts:
        hearts.sort(key=lambda x: rank_value[x[1][0]], reverse=True)
        idx = hearts[0][0]
        return computer_hand.pop(idx)
    
    # 否則優先攻擊
    if attacks:
        attacks.sort(key=lambda x: rank_value[x[1][0]], reverse=True)
        idx = attacks[0][0]
        return computer_hand.pop(idx)
    
    # 有方塊就出方塊
    if diamonds:
        diamonds.sort(key=lambda x: rank_value[x[1][0]], reverse=True)
        idx = diamonds[0][0]
        return computer_hand.pop(idx)
    
    # 都沒有就出紅心
    if hearts:
        hearts.sort(key=lambda x: rank_value[x[1][0]], reverse=True)
        idx = hearts[0][0]
        return computer_hand.pop(idx)
    
    # 隨機出牌（備用）
    idx = random.randint(0, len(computer_hand) - 1)
    return computer_hand.pop(idx)

# ===== 玩家 vs 玩家 模式的函數 =====
def pick_card_hidden(player_num, hand):
    """玩家隱藏選牌（雙人模式用）"""
    clear()
    print(f"====== 玩家{player_num} 請看你的手牌（不要讓對方看到） ======\n")
    print(hand_string(hand))
    choice = input(f"\n玩家{player_num}，請選擇要出的牌編號（1-5）： ")

    while not choice.isdigit() or not (1 <= int(choice) <= len(hand)):
        choice = input("編號錯誤，請重新輸入（1-5）： ")

    picked = hand.pop(int(choice) - 1)
    clear()  # 出牌後立即隱藏
    return picked

# ===== 玩家 vs 電腦 遊戲流程 =====
def play_vs_computer():
    """執行玩家對電腦的遊戲模式"""
    deck = create_deck()
    player_hp = 25
    computer_hp = 25
    player_hand = [deck.pop() for _ in range(5)]
    computer_hand = [deck.pop() for _ in range(5)]
    round_num = 1

    print("\n" + "=" * 50)
    print("       撲克牌對戰遊戲（玩家 vs 電腦）")
    print("=" * 50)
    print("\n遊戲規則：")
    print("  ♠♣ 黑桃/梅花 → 攻擊對方")
    print("  ♥ 紅心 → 回復自己血量")
    print("  ♦ 方塊 → 反擊（對方攻擊時反彈傷害）")
    print(f"\n雙方初始 HP：25")
    input("\n按 Enter 開始遊戲...")

    while player_hp > 0 and computer_hp > 0 and (player_hand or computer_hand):
        print("\n" + "=" * 50)
        print(f"第 {round_num} 回合")
        print("=" * 50)
        print(f"你的 HP：{player_hp}　　電腦 HP：{computer_hp}")
        print(f"牌庫剩餘：{len(deck)} 張")

        # 玩家選牌
        player_card = player_pick_card(player_hand)
        # 電腦選牌
        computer_card = computer_pick_card(computer_hand, player_hp, computer_hp)

        r1, s1 = player_card
        r2, s2 = computer_card
        v1 = rank_value[r1]
        v2 = rank_value[r2]

        print("\n----- 回合結果 -----")
        print(f"你出牌：{r1}{s1}")
        print(f"電腦出牌：{r2}{s2}")

        # 回血
        if s1 == "♥":
            player_hp += v1
            print(f"★ 你使用紅心回血 +{v1} → HP: {player_hp}")
        if s2 == "♥":
            computer_hp += v2
            print(f"★ 電腦使用紅心回血 +{v2} → HP: {computer_hp}")

        # 反擊
        if s1 == "♦" and s2 in ["♠", "♣"]:
            computer_hp -= v2
            print(f"★ 你的方塊反擊成功！電腦 -{v2} → HP: {computer_hp}")
        if s2 == "♦" and s1 in ["♠", "♣"]:
            player_hp -= v1
            print(f"★ 電腦方塊反擊！你 -{v1} → HP: {player_hp}")

        # 正常攻擊
        if s1 in ["♠", "♣"] and s2 != "♦":
            computer_hp -= v1
            print(f"★ 你的攻擊命中！電腦 -{v1} → HP: {computer_hp}")
        if s2 in ["♠", "♣"] and s1 != "♦":
            player_hp -= v2
            print(f"★ 電腦攻擊命中！你 -{v2} → HP: {player_hp}")

        # 補牌
        draw_card_if_needed(player_hand, deck)
        draw_card_if_needed(computer_hand, deck)
        
        input("\n按 Enter 進入下一回合...")
        round_num += 1

    # 遊戲結果
    print("\n" + "=" * 50)
    print("遊戲結束")
    print("=" * 50)
    if player_hp <= 0 and computer_hp <= 0:
        print("平手！雙方同時倒下！")
    elif player_hp <= 0:
        print("電腦勝利！你輸了...")
    elif computer_hp <= 0:
        print("恭喜！你贏了！")
    else:
        if player_hp > computer_hp:
            print(f"牌用完了！你的 HP ({player_hp}) 較高 → 你贏了！")
        elif computer_hp > player_hp:
            print(f"牌用完了！電腦 HP ({computer_hp}) 較高 → 電腦勝利！")
        else:
            print("牌用完了！HP 相同 → 平手！")

# ===== 玩家 vs 玩家 遊戲流程 =====
def play_vs_player():
    """執行雙人對戰的遊戲模式（含隱藏手牌機制）"""
    deck = create_deck()
    player1_hp = 25
    player2_hp = 25
    player1 = [deck.pop() for _ in range(5)]
    player2 = [deck.pop() for _ in range(5)]
    round_num = 1

    print("\n===== 撲克牌對戰遊戲（玩家 vs 玩家）！ =====")
    print("\n遊戲規則：")
    print("  ♠♣ 黑桃/梅花 → 攻擊對方")
    print("  ♥ 紅心 → 回復自己血量")
    print("  ♦ 方塊 → 反擊（對方攻擊時反彈傷害）")
    print(f"\n雙方初始 HP：25")
    input("\n按 Enter 開始...")

    while player1_hp > 0 and player2_hp > 0 and (player1 or player2):
        print(f"\n===== 第 {round_num} 回合 =====")
        print(f"玩家1 HP：{player1_hp}")
        print(f"玩家2 HP：{player2_hp}")
        print(f"牌庫剩餘：{len(deck)}")

        # 玩家1選牌
        card1 = pick_card_hidden(1, player1)
        # 玩家2選牌
        card2 = pick_card_hidden(2, player2)

        r1, s1 = card1
        r2, s2 = card2
        v1 = rank_value[r1]
        v2 = rank_value[r2]

        print("\n===== 回合結果 =====")
        print(f"玩家1 出牌：{r1}{s1}")
        print(f"玩家2 出牌：{r2}{s2}")

        # 回血
        if s1 == "♥":
            player1_hp += v1
            print(f"玩家1 使用紅心回血 +{v1} → HP: {player1_hp}")
        if s2 == "♥":
            player2_hp += v2
            print(f"玩家2 使用紅心回血 +{v2} → HP: {player2_hp}")

        # 反擊
        if s1 == "♦" and s2 in ["♠", "♣"]:
            player2_hp -= v2
            print(f"玩家1 方塊反擊 → 玩家2 -{v2} → HP: {player2_hp}")
        if s2 == "♦" and s1 in ["♠", "♣"]:
            player1_hp -= v1
            print(f"玩家2 方塊反擊 → 玩家1 -{v1} → HP: {player1_hp}")

        # 正常攻擊
        if s1 in ["♠", "♣"] and s2 != "♦":
            player2_hp -= v1
            print(f"玩家1 攻擊 → 玩家2 -{v1} → HP: {player2_hp}")
        if s2 in ["♠", "♣"] and s1 != "♦":
            player1_hp -= v2
            print(f"玩家2 攻擊 → 玩家1 -{v2} → HP: {player1_hp}")

        # 補牌
        draw_card_if_needed(player1, deck)
        draw_card_if_needed(player2, deck)
        input("\n按 Enter 進入下一回合...")
        round_num += 1
        clear()

    # 遊戲結果
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

# ===== 主選單 =====
def main():
    """遊戲主選單：選擇遊戲模式"""
    while True:
        print("\n" + "=" * 50)
        print("       ♠ ♥ 撲克牌對戰遊戲 ♦ ♣")
        print("=" * 50)
        print("\n請選擇遊戲模式：")
        print("  1. 玩家 vs 電腦")
        print("  2. 玩家 vs 玩家")
        print("  3. 離開遊戲")
        
        choice = input("\n請輸入選項（1-3）： ")
        
        if choice == "1":
            play_vs_computer()
        elif choice == "2":
            play_vs_player()
        elif choice == "3":
            print("\n感謝遊玩，再見！")
            break
        else:
            print("無效選項，請重新輸入！")
        
        # 遊戲結束後詢問是否再玩一次
        if choice in ["1", "2"]:
            again = input("\n要再玩一次嗎？（y/n）： ")
            if again.lower() != "y":
                print("\n感謝遊玩，再見！")
                break

if __name__ == "__main__":
    main()

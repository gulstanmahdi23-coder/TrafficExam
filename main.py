import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import random
import time
import os
import msvcrt

# ============ ڕێکخستنەکان ============
TOTAL_QUESTIONS = 25
TIME_PER_QUESTION = 60  # چرکە
PASS_PERCENTAGE = 80
IMAGES_FOLDER = "images"
MARKS_PER_QUESTION = 4

def load_questions_for_group(group_num):
    """خوێندنەوەی پرسیارەکانی گرووپێکی دیاریکراو"""
    filename = f"group{group_num}.csv"
    all_questions = []
    
    if not os.path.exists(filename):
        print(f"❌ فایلی {filename} نەدۆزرایەوە!")
        return all_questions

    try:
        df = pd.read_csv(filename, encoding='utf-8-sig', header=None)
    except Exception as e:
        print(f"❌ هەڵە لە خوێندنەوەی فایل {filename}: {e}")
        return all_questions

    for idx, row in df.iterrows():
        question = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        if not question or question.lower() == "nan":
            continue

        options = []
        for col in [1, 2, 3]:
            if len(row) > col and pd.notna(row.iloc[col]):
                options.append(str(row.iloc[col]).strip())

        if len(options) < 3:
            continue

        correct_idx = 0
        if len(row) > 4 and pd.notna(row.iloc[4]):
            ans_str = str(row.iloc[4]).strip()
            if ans_str:
                first = ans_str[0].upper()
                if first in "ABC":
                    correct_idx = ord(first) - ord('A')

        image =""
        if len(row) > 5 and pd.notna(row.iloc[5]):
            img = str(row.iloc[5]).strip()
            if img.lower() != "nan":
                image = img

        all_questions.append({
            "question": question,
            "options": options,
            "correct": correct_idx,
            "image": image,
        })
        
    return all_questions


def get_answer_with_timeout(timeout):
    """وەرگرتنی وەڵام لەگەڵ کاتژمێری سنووردار"""
    start = time.time()
    last_shown = -1

    while time.time() - start < timeout:
        elapsed = time.time() - start
        remaining = int(timeout - elapsed)

        if remaining != last_shown and remaining % 5 == 0:
            print(f"\r⏱️ کاتی ماوە: {remaining:2d} چرکە    ", end="", flush=True)
            last_shown = remaining

        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8', errors='ignore').upper()
            if char in ['A', 'B', 'C']:
                return char
            elif char == '1':
                return 'A'
            elif char == '2':
                return 'B'
            elif char == '3':
                return 'C'
        time.sleep(0.05)

    return None


def run_exam():
    """بەڕێوەبردنی تاقیکردنەوە"""
    print("=" * 60)
    print("🚦 سیستەمی تاقیکردنەوەی هاتوچۆی هەرێمی کوردستان")
    print("=" * 60)
    print()

    # دیاریکردنی گرووپ لەلایەن بەکارهێنەرەوە (1 بۆ 4)
    while True:
        try:
            group_choice = int(input("👉 تکایە ژمارەی گرووپ هەڵبژێرە (لە 1 بۆ 4): "))
            if group_choice in [1, 2, 3, 4]:
                break
            else:
                print("❌ تکایە تەنها ژمارەیەک لە نێوان 1 بۆ 4 هەڵبژێرە.")
        except ValueError:
            print("❌ تکایە تەنها ژمارە بنووسە.")

    print()
    print(f"📚 بارکردنی پرسیارەکانی گرووپی {group_choice}...")
    all_questions = load_questions_for_group(group_choice)

    if not all_questions:
        print(f"❌ هیچ پرسیارێک لە گرووپی {group_choice} نەدۆزرایەوە یان فایلەکە نییە.")
        return

    if len(all_questions) < TOTAL_QUESTIONS:
        print(f"❌ تەنها {len(all_questions)} پرسیار لەم گرووپەدا هەیە، {TOTAL_QUESTIONS} پێویستە.")
        return

    print(f"✅ {len(all_questions)} پرسیار بۆ گرووپی {group_choice} بارکران")
    print()
    while True:
        try:
            group_choice = int(input("👉 تکایە ژمارەی گرووپ هەڵبژێرە (لە 1 بۆ 4): "))
            if group_choice in [1, 2, 3, 4]:
                break
            else:
                print("❌ تکایە تەنها ژمارەیەک لە نێوان 1 بۆ 4 هەڵبژێرە.")
        except ValueError:
            print("❌ تکایە تەنها ژمارە بنووسە.")

    print()
    print(f"📚 بارکردنی پرسیارەکانی گرووپی {group_choice}...")
    
    # ئینجا لێرەدا فەنکشنەکە بانگ بکە:
    group_choice=1
    all_questions=[]
    all_questions = load_questions_for_group(group_choice)
    # هەڵبژاردنی ٢٥ پرسیار بە هەڵکەوت لەو گرووپە
    selected=random.sample(all_questions,TOTAL_QUESTIONS)

    for q in selected:
        correct_text = q["options"][q["correct"]]
        shuffled = q["options"][:]
        random.shuffle(shuffled)
        q["options"] = shuffled
        q["correct"] = shuffled.index(correct_text)

print(f"🎯{TOTAL_QUESTIONS} پرسیار بە هەڵکەوت لە گرووپی group_choice هەڵبژێردران")
print(f"⏱️ کاتی هەر پرسیارێک: {TIME_PER_QUESTION} چرکە")
print(f"📊 ئاستی دەرچوون: {PASS_PERCENTAGE}%")
print()
input("▶️ Enter دابگرە بۆ دەستپێکردنی تاقیکردنەوە...")
print()

score = 0
group_choice=1
all_questions=load_questions_for_group(group_choice)
selected=random.sample(all_questions,TOTAL_QUESTIONS)
for i, q in enumerate(selected,1):
        print("=" * 60)
        print(f"❓ پرسیار {i} لە {TOTAL_QUESTIONS} (گرووپی group_choice )")
        print("=" * 60)
        print()

        # پشکنینی وێنە بە شێوازێکی زۆر سەلامەت
        img_name = q.get("image", "")
        if img_name and str(img_name).lower() != "nan":
            img_path = os.path.join(IMAGES_FOLDER, str(img_name))
            if os.path.exists(img_path):
                print(f"📸 وێنە: {img_name}")
                try:
                    os.startfile(img_path)
                except Exception:
                    pass
            else:
                print(f"⚠️ وێنە نەدۆزرایەوە: {img_name}")
            print()

        # پرسیار
        print(f"📝 {q['question']}")
        print()

        # هەڵبژاردنەکان
        for j, opt in enumerate(q["options"]):
            letter = chr(65 + j)
            print(f"  {letter}) {opt}")
        print()

        print(f"👉 وەڵام هەڵبژێرە (A / B / C)")
        print(f"⏱️ کات: {TIME_PER_QUESTION} چرکە")
        print("👉 ", end="", flush=True)

        user_answer = get_answer_with_timeout(TIME_PER_QUESTION)

        if user_answer is None:
            print("\r⏱️ کاتەکە تەواو بوو!                           ")
            print(f"    ❌ وەڵام نەدرا (وەک هەڵە دەژمێردرێت)")
        else:
            user_idx = ord(user_answer) - ord('A')
            if user_idx == q["correct"]:
                score += 1
                print(f"\r✅ وەڵامی ڕاست!                                 ")
            else:
                correct_letter = chr(65 + q["correct"])
                print(f"\r❌ هەڵە! وەڵامی ڕاست: {correct_letter}                 ")

        print()
        time.sleep(1)

    # ============ ئەنجام ============
print()
print("=" * 60)
print(f"📊 ئەنجامی کۆتایی تاقیکردنەوەی گرووپی group_choice")
print("=" * 60)
print()

percentage = (score / TOTAL_QUESTIONS) * 100

print(f"✅ وەڵامی ڕاست: {score}")
print(f"❌ وەڵامی هەڵە: {TOTAL_QUESTIONS - score}")
print(f"📈 ڕێژە: {percentage:.1f}%")
print()

if percentage >= PASS_PERCENTAGE:
        print("🎉 پیرۆزە! تۆ دەرچوویت!")
        print(f"    ({percentage:.1f}% ≥ {PASS_PERCENTAGE}%)")
else:
        print("😔 بەداخەوە، تۆ دەرنەچوویت.")
        print(f"    ({percentage:.1f}% < {PASS_PERCENTAGE}%)")

print()
print("=" * 60)


if __name__ == "__main__":
    run_exam()
import io
import json
import os
import random
import sys
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import msvcrt
import pandas as pd

# ============ ڕێکخستنەکان ============
TOTAL_QUESTIONS = 25
TIME_PER_QUESTION = 60  # چرکە
PASS_PERCENTAGE = 80
IMAGES_FOLDER = "images"
MARKS_PER_QUESTION = 4


def load_questions_for_group(group_num):
    """خوێندنەوەی پرسیارەکان: یەکەمجار لە questions.json، ئەگەر نەبوو لە CSV"""
    all_questions = []
    group_key = str(group_num)

    # 1. هەوڵدان بۆ خوێندنەوە لە فایلی questions.json
    if os.path.exists("questions.json"):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if group_key in data:
                    for q in data[group_key]:
                        options = [
                            q.get("choice1", ""),
                            q.get("choice2", ""),
                            q.get("choice3", ""),
                        ]
                        correct_ans_str = q.get("correctAnswer", "1")
                        correct_idx = (
                            int(correct_ans_str) - 1
                            if correct_ans_str.isdigit()
                            else 0
                        )

                        all_questions.append({
                            "question": q.get("question", ""),
                            "options": options,
                            "correct": correct_idx,
                            "image": q.get("image", "none"),
                        })
                    if all_questions:
                        return all_questions
        except Exception:
            pass

    # 2. ئەگەر JSON نەبوو یان سەرکەوتوو نەبوو، لە CSV دەخوێنێتەوە
    filename = f"group{group_num}.csv"
    if not os.path.exists(filename):
        print(f"❌ نە فایلی {filename} و نە فایلی questions.json نەدۆزرایەوە!")
        return all_questions

    try:
        df = pd.read_csv(filename, encoding="utf-8-sig", header=None)
    
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
                    correct_idx = ord(first) - ord("A")

        image = "none"
        if len(row) > 5 and pd.notna(row.iloc[5]):
            img = str(row.iloc[5]).strip()
            if img.lower() != "nan" and img != "":
                image = img

        all_questions.append({
            "question": question,
            "options": options,
            "correct": correct_idx,
            "image": image,
        })

    return all_questions


def generate_json_for_web():
    all_groups_data = {}
    for i in range(1, 5):
        filename = f"group{i}.csv"
        q_list = []
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename, encoding="utf-8-sig", header=None)
                for idx, row in df.iterrows():

                    if len(row)<4 or pd.isna(row.iloc[0]):continue
                    question =(str(row.iloc[0]).strip()if pd.notna(row.iloc[0])else "")
                    if not question or question.lower() == "nan"or "column1"in question.lower():
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
                                correct_idx = ord(first) - ord("A")
                    image = "none"
                    if len(row) > 5 and pd.notna(row.iloc[5]):
                        img = str(row.iloc[5]).strip()
                        if img.lower() != "nan" and img != "":
                            image = img

                    q_list.append({
                        "question": question,
                        "choice1": options[0] if len(options) > 0 else "",
                        "choice2": options[1] if len(options) > 1 else "",
                        "choice3": options[2] if len(options) > 2 else "",
                        "correctAnswer": str(correct_idx + 1),
                        "image": image,
                    })
            except Exception:
                pass

        all_groups_data[str(i)] = q_list

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(all_groups_data, f, ensure_ascii=False, indent=4)
    print(
        "🌐 فایلی questions.json بە سەرکەوتوویی لە CSVـیەکانەوە نوێ کرایەوە بۆ"
        " وێبسایت!"
    )


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
            char = msvcrt.getch().decode("utf-8", errors="ignore").upper()
            if char in ["A", "B", "C"]:
                return char
            elif char == "1":
                return "A"
            elif char == "2":
                return "B"
            elif char == "3":
                return "C"
        time.sleep(0.05)
    return None


def run_exam():
    print("تاقیکردنەوە:فەنکشنیrun_examدەستی پێکرد")  
    generate_json_for_web()
    print()
    print("=" * 60)
    print("🚦 سیستەمی تاقیکردنەوەی هاتوچۆی هەرێمی کوردستان")
    print("=" * 60)
    print()

    while True:
        try:
            group_choice = int(
                input("👉 تکایە ژمارەی گرووپ هەڵبژێرە (لە 1 بۆ 4): ")
            )
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
        print(
            f"❌ هیچ پرسیارێک لە گرووپی {group_choice} نەدۆزرایەوە یان فایلەکە نییە."
        )
        return

    if len(all_questions)<TOTAL_QUESTIONS:
        print(
        f"❌ تەنها {len(all_questions)} پرسیار هەیە، پێویستە{TOTAL_QUESTIONS}"
            " هەبێت."
        )
        return

    print(f"✅{len(all_questions)} پرسیار بۆ گرووپی{group_choice} بارکران")
    print()

    # هەڵبژاردنی ٢٥ پرسیار بە هەڵکەوت لەو گرووپە
    selected = random.sample(all_questions,TOTAL_QUESTIONS)
    for q in selected:
        correct_text = q["options"][q["correct"]]
        shuffled=q["options"][:]
        random.shuffle(shuffled)
        q["options"]=shuffled
        q["correct"]=shuffled.index(correct_text)

    print(
        f"🎯{TOTAL_QUESTIONS}پرسیار بە هەڵکەوت لە گرووپی{group_choice}"
        " هەڵبژێردران")
    print(f"⏱️کاتی هەر پرسیارێک:{TIME_PER_QUESTION}چرکە")
    print(f"📊ئاستی دەرچوون:{PASS_PERCENTAGE}%")
    print()
    input("▶ Enterدابگرە بۆ دەستپێکردنی تاقیکردنەوە...")
    print()

    score = 0
    for i, q in enumerate(selected,1):
        print("=" * 60)
        print(f"❓پرسیار{i}لە{TOTAL_QUESTIONS}(گرووپی{group_choice})")
        print("=" * 60)
        print()

        # پشکنینی وێنە
        img_name=q.get("image","")
        if img_name and str(img_name).lower()!="none"and str(img_name)!= "":
            img_path=os.path.join(IMAGES_FOLDER,str(img_name))
            if os.path.exists(img_path):
                print(f"📸وێنە:{img_name}")
                try:
                    os.startfile(img_path)
                except Exception:
                    pass
            else:
                print(f"⚠️وێنە نەدۆزرایەوە:{img_name}")
            print()

        # پرسیار
        print(f"📝{q['question']}")
        print()

        # هەڵبژاردنەکان
        for j,opt in enumerate(q["options"]):
            letter=chr(65+j)
            print(f"{letter}){opt}")
        print()

        print(f"👉وەڵام هەڵبژێرە(A / B / C)")
        print(f"⏱️کات:{TIME_PER_QUESTION}چرکە")
        print("👉", end="",flush=True)
        user_answer=get_answer_with_timeout(TIME_PER_QUESTION)

        if user_answer is None:
            print("\r⏱️کاتەکە تەواو بوو!")
            print("❌وەڵام نەدرا(وەک هەڵە دەژمێردرێت)")
        else:
            user_idx=ord(user_answer)-ord("A")
            if user_idx==q["correct"]:
                score+=1
                print("\r✅وەڵامی ڕاست!")
            else:
                correct_letter=chr(65+q["correct"])
                print(f"\r❌هەڵە! وەڵامی ڕاست:{correct_letter}")

        print()

    time.sleep(1)

    print()
    print("="*60)
    print(f"📊 ئەنجامی کۆتایی تاقیکردنەوەی گرووپی{group_choice}")
    print("="*60)
    print()

    percentage=(score/TOTAL_QUESTIONS)*100

    print(f"✅وەڵامی ڕاست:{score}")
    print(f"❌وەڵامی هەڵە:{TOTAL_QUESTIONS-score}")
    print(f"📈ڕێژە:{percentage:.1f}%")
    print()

    if percentage>=PASS_PERCENTAGE:
        print("🎉پیرۆزە! تۆ دەرچوویت!")
        print(f"({percentage:.1f}%≥{PASS_PERCENTAGE}%)")
    else:
        print("😔بەداخەوە، تۆ دەرنەچوویت.")
        print(f"({percentage:.1f}%<{PASS_PERCENTAGE}%)")

    print()
    print("=" * 60)
if __name__ == "__main__":
      run_exam()
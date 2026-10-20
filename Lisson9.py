import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import os
import time

# БОЛЬШЕ СЛОВ ДЛЯ КАЖДОГО УРОВНЯ
WORDS = {
    1: {
        "кот": "cat", "дом": "house", "собака": "dog", "вода": "water", 
        "яблоко": "apple", "солнце": "sun", "машина": "car", "книга": "book",
        "стол": "table", "стул": "chair", "молоко": "milk", "хлеб": "bread",
        "ручка": "pen", "окно": "window", "дверь": "door", "город": "city"
    }, 
    2: {
        "дерево": "tree", "друг": "friend", "школа": "school", "цветок": "flower", 
        "небо": "sky", "река": "river", "гора": "mountain", "море": "sea",
        "птица": "bird", "рыба": "fish", "время": "time", "музыка": "music",
        "погода": "weather", "работа": "work", "деньги": "money", "игра": "game"
    }, 
    3: {
        "приключение": "adventure", "воображение": "imagination", "ответственность": "responsibility", 
        "университет": "university", "технология": "technology", "возможность": "opportunity",
        "информация": "information", "образование": "education", "празднование": "celebration",
        "достижение": "achievement", "преимущество": "advantage", "безопасность": "security",
        "окружающая среда": "environment", "оборудование": "equipment", "исследование": "research"
    }
}

def record_and_recognize(sec):
    print("  ┌──────────────────────────────────────┐")
    print(f"  │  🎤 [ЗАПИСЬ] Говорите ({sec} сек)...      │")
    print("  └──────────────────────────────────────┘")
    
    myrecording = sd.rec(int(sec * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()
    wav.write("t.wav", 44100, myrecording)
    
    print("  ┌──────────────────────────────────────┐")
    print("  │  ⏳ [АНАЛИЗ] Распознаем речь...       │")
    print("  └──────────────────────────────────────┘")
    
    r = sr.Recognizer()
    try:
        with sr.AudioFile("t.wav") as s:
            return r.recognize_google(r.record(s), language="en-US").lower()
    except:
        return ""
    finally:
        os.remove("t.wav")

# --- КРУТОЙ ИНТЕРФЕЙС ---
print(r"""
  ██████╗  █████╗ ███╗   ███╗███████╗
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
 ██║  ███╗███████║██╔████╔██║█████╗  
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
       ГОЛОСОВОЙ ПЕРЕВОДЧИК
""")

print(" ╔══════════════════════════════════════════╗")
print(" ║  Выберите уровень сложности:             ║")
print(" ║  1. 🟢 Легкий   (5 жизней, 5 сек)         ║")
print(" ║  2. 🟡 Средний  (3 жизни, 4 сек)          ║")
print(" ║  3. 🔴 Сложный  (1 жизнь, 3 сек)          ║")
print(" ╚══════════════════════════════════════════╝")

lvl_choice = input("  Ваш выбор (1/2/3): ")
lvl = int(lvl_choice) if lvl_choice in ['1', '2', '3'] else 1

lives, sec = (5, 5) if lvl == 1 else (3, 4) if lvl == 2 else (1, 3)
max_lives = lives 
score = 0
words_list = list(WORDS[lvl].items())
random.shuffle(words_list) # Перемешиваем расширенный список

print("\n 🚀 Игра начинается! Произносите перевод слов на английском.\n")

for ru, en in words_list:
    if lives <= 0: break
    
    hearts = '♥️ ' * lives + '♡ ' * (max_lives - lives)
    print(f"\n  ❤️  Жизни: {hearts}| 🏆 Очки: {score}")
    print(" ╭──────────────────────────────────────────╮")
    print(f" │  👉 Переведите слово: {ru.upper():<18} │")
    print(" ╰──────────────────────────────────────────╯")
    
    input("  [Нажмите ENTER, чтобы говорить]...")
    
    start_time = time.time()
    ans = record_and_recognize(sec)
    reaction_time = time.time() - start_time
    
    if ans:
        print(f"\n  🗣️ Вы сказали: \"{ans}\"")
        
    if en in ans:
        bonus = 5 if reaction_time < 3.0 else 0
        score += 10 + bonus
        print(f"  ✅  ОТЛИЧНО! +10 очков" + (f" и +5 за скорость! ⚡" if bonus else ""))
    else:
        print(f"  ❌  ОШИБКА! Правильный ответ: '{en}'")
        lives -= 1

# --- КОНЕЦ ИГРЫ ---
print("\n ╔══════════════════════════════════════════╗")
if lives <= 0:
    print(" ║  💀  GAME OVER  💀                       ║")
else:
    print(" ║  🎉  ПОБЕДА! Вы прошли игру!             ║")
print(f" ║  🏆  Ваш итоговый счет: {score:<5} очков.        ║")
print(" ╚══════════════════════════════════════════╝")
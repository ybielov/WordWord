import pygame
import sys
import random
import itertools
import os
from buttons import ImageButton
from pygame.constants import MOUSEBUTTONDOWN
from pygame.constants import FINGERDOWN
from kivy.utils import platform

#Імпортування nltk
import nltk
nltk.data.path.append('./nltk_data')
from nltk.corpus import words
from nltk.corpus import wordnet as wn
nltk.download('words', download_dir='./nltk_data')
nltk.download('wordnet', download_dir='./nltk_data')


word_list = words.words()
vowels = set("aeiou")
score_table = []

#Ініціалізація pygame
pygame.init()

#Завантаження асетів
background = os.path.abspath("images/background.jpg")
disabled = os.path.abspath("images/disabled.jpg")
exit_empty = os.path.abspath("images/exit_empty.jpg")
logo = os.path.abspath("images/logo.png")
play_empty= os.path.abspath("images/play_empty.jpg")

#Ініціалізація вікна
if platform == "android":
    screen_size = pygame.display.Info()
    WIDTH, HEIGHT = (screen_size.current_w, screen_size.current_h)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
else:
    WIDTH, HEIGHT = (1000, 550)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
logo = pygame.image.load("images/logo.png")
pygame.display.set_caption("WordWord")

#Додання фонового зображення
background = pygame.image.load(background)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#Створення кнопок
play_button = ImageButton(WIDTH/2-275/2, 100, 275, 66, "Play", play_empty, False)
score_button = ImageButton(WIDTH/2-275/2, 176, 275, 66, "Score Table", play_empty, False)
exit_button = ImageButton(WIDTH/2-275/2, 252, 275, 66, "Exit", exit_empty, False)
enter_button = ImageButton(WIDTH-93, 400, 90, 50, "Enter", play_empty, False)
clear_button = ImageButton(3, 400, 90, 50, "Clear", exit_empty, False)
enter_field = ImageButton(0, 347, WIDTH, 50, None, play_empty, False)
menu_back = ImageButton(WIDTH / 2 - 100, HEIGHT - 70, 200, 50, "Back", exit_empty, False)
definition_label = ImageButton(WIDTH-215, 52, 200, 250, " ", play_empty, False)

letter_points = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 8, 'x': 8,
    'q': 10, 'z': 10
}

#Функція створення головного меню
def main_menu():
    screen.blit(background, (0, 0))
    screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #Почати гру
            if event.type == pygame.USEREVENT and event.button == play_button:
                select_mode()

            if event.type == pygame.USEREVENT and event.button == score_button:
                show_score()

            #Вихід з гри
            if event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()

            play_button.handle_event(event)
            score_button.handle_event(event)
            exit_button.handle_event(event)

        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen)
        score_button.check_hover(pygame.mouse.get_pos())
        score_button.draw(screen)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
        pygame.display.flip()

def select_mode():
    running = True

    global mode

    easy_button = ImageButton(WIDTH / 2 - 275 / 2, 100, 275, 66, "Easy", play_empty, False)
    medium_button = ImageButton(WIDTH / 2 - 275 / 2, 176, 275, 66, "Medium", play_empty, False)
    hard_button = ImageButton(WIDTH / 2 - 275 / 2, 252, 275, 66, "Hard", play_empty, False)
    back_button = ImageButton(WIDTH / 2 - 275 / 2, 328, 275, 66, "Back", exit_empty, False)

    while running:
        screen.blit(background, (0, 0))

        title_font = pygame.font.Font(None, 40)
        title_text = title_font.render("Select difficulty level:", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 55))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                if event.button == easy_button:
                    mode = "easy"
                    game(mode)
                elif event.button == medium_button:
                    mode = "medium"
                    game(mode)
                elif event.button == hard_button:
                    mode = "hard"
                    game(mode)

            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()

            easy_button.handle_event(event)
            medium_button.handle_event(event)
            hard_button.handle_event(event)
            back_button.handle_event(event)


        easy_button.check_hover(pygame.mouse.get_pos())
        easy_button.draw(screen)

        medium_button.check_hover(pygame.mouse.get_pos())
        medium_button.draw(screen)

        hard_button.check_hover(pygame.mouse.get_pos())
        hard_button.draw(screen)

        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        pygame.display.flip()

def calculate(word):
    return sum(letter_points.get(letter, 0) for letter in word.lower())

def is_regular_plural(word, all_words):
    if word.endswith('ies'):
        singular = word[:-3] + 'y'
        return singular in all_words
    elif word.endswith('es'):
        singular = word[:-2]
        if singular.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return singular in all_words
    elif word.endswith('s') and not word.endswith('ss'):
        singular = word[:-1]
        return singular in all_words
    return False

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def game(mode):
    running = True

    picked_words = []
    for w in word_list:
        w = w.lower()
        word_vowels = [char for char in w if char in vowels]
        if mode == "easy":
            if len(word_vowels) == 4 and len(set(word_vowels)) == 4:
                if len(w) == 10 and w.isalpha():
                    picked_words.append(w)
                    total_time = 180
        elif mode == "medium":
            if 8 <= len(w) <= 9 and w.isalpha():
                picked_words.append(w)
                total_time = 150
        elif mode == "hard":
            if len(w) == 7 and w.isalpha():
                if len(word_vowels) == 2 and len(set(word_vowels)) == 2:
                    picked_words.append(w)
                    total_time = 120

    #Випадкове слово для раунду
    word = random.choice(picked_words)
    word = word.lower()

    #Словник для перевірки
    all_words = set(word_list)

    #Множина для анаграм
    possible = set()

    #Алгоритм пошуку анаграм
    for i in range(2, len(word) + 1):
        permutations = itertools.permutations(word, i)
        for p in permutations:
            anagram = ''.join(p)
            if (anagram in all_words
                    and anagram != word
                    and anagram == anagram.lower()
                    and not is_regular_plural(anagram, all_words)):
                    possible.add(anagram)
    possible = sorted(possible)

    enter = []
    found_words = []
    score = []

    #Кнопки для літер
    x0 = WIDTH / 2 - (len(word) * (50 + 3)) / 2
    buttons = []
    for l in word:
        letter_button = ImageButton(x0, 400, 50, 50, l, play_empty, False)
        buttons.append(letter_button)
        x0 += 53

    start_ticks = pygame.time.get_ticks()
    font_timer = pygame.font.Font(None, 36)

    # Флаг, чтобы выполнить действие один раз по завершению таймера
    time_over = False

    while running:
        # Очищення екрану
        screen.blit(background, (0,0))

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if not button.disabled and button.rect.collidepoint(event.pos):
                        enter.append(button.text)
                        enter_field.text = ''.join(enter)
                        button.disable()

                for word_label in found_words:
                    if word_label.rect.collidepoint(event.pos):
                        selected_word = word_label.text
                        synsets = wn.synsets(selected_word)
                        if synsets:
                            syn = synsets[0]
                            pos = syn.pos()
                            meaning = syn.definition()
                            pos_dict = {
                                'n': 'n.',
                                'v': 'v.',
                                'a': 'adj.',
                                's': 'adj.',
                                'r': 'adv.'
                            }
                            definition = f"{selected_word} ({pos_dict.get(pos, pos)}) - {meaning}"
                        else:
                            definition = f"{selected_word} - definition not found"

                        definition_label.text = definition

            if event.type == pygame.USEREVENT and event.button == clear_button:
                enter.clear()
                enter_field.text = ""
                for button in buttons:
                    button.reset()

            if event.type == pygame.USEREVENT and event.button == enter_button:
                entered = enter_field.text.strip().lower()

                if entered in possible and entered not in [w.text for w in found_words]:
                    index = len(found_words)
                    x = 3 + (index % 9) * 75
                    y = 45 + (index // 9) * 35

                    word_label = ImageButton(x, y, 70, 30, entered, play_empty, False)
                    found_words.append(word_label)

                    points = calculate(entered)
                    score.append(points)

                    enter.clear()
                    enter_field.text = ""
                    for button in buttons:
                        button.reset()

            clear_button.handle_event(event)
            enter_button.handle_event(event)

        # Відмальовування кнопок
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        enter_button.check_hover(pygame.mouse.get_pos())
        enter_button.draw(screen)

        clear_button.check_hover(pygame.mouse.get_pos())
        clear_button.draw(screen)

        enter_field.check_hover(pygame.mouse.get_pos())
        enter_field.draw(screen)

        definition_text = definition_label.text
        definition_label.text = None
        definition_label.draw(screen)

        if definition_text:
            font_def = pygame.font.Font(None, 25)
            lines = wrap_text(definition_text, font_def, definition_label.rect.width - 10)
            max_lines = (definition_label.rect.height - 10) // font_def.get_linesize()

            for i, line in enumerate(lines[:max_lines]):
                text_surface = font_def.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (
                    definition_label.rect.x + 5,
                    definition_label.rect.y + 5 + i * font_def.get_linesize()
                ))
        definition_label.text = definition_text

        for word_label in found_words:
            word_label.check_hover(mouse_pos)
            word_label.draw(screen)

        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, total_time - seconds_passed)

        minutes = time_left // 60
        seconds = time_left % 60

        if time_left <= 10:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        timer_text = font_timer.render(f"{minutes:02}:{seconds:02}", True, color)

        timer_bg = pygame.Rect(WIDTH - 115, 2, 100, 40)
        pygame.draw.rect(screen, (255, 255, 255), timer_bg, border_radius=8)
        pygame.draw.rect(screen, (91, 157, 16), timer_bg, 2, border_radius=8)
        screen.blit(timer_text, (WIDTH - 100, 10))

        score_bg = pygame.Rect(WIDTH/2 - 100, 2, 200, 30)
        pygame.draw.rect(screen, (255, 255, 255), score_bg, border_radius=8)
        pygame.draw.rect(screen, (91, 157, 16), score_bg, 2, border_radius=8)
        font = pygame.font.Font(None, 28)

        score_text = font.render(f"Score: {sum(score)}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))


        if time_left == 0 and not time_over:
            global round_data
            round_data = []
            time_over = True
            score_table.append((word, mode, len(found_words), sum(score)))
            round_data.append((word, mode, len(found_words), sum(score)))
            pygame.time.delay(500)
            show_results(round_data)

        pygame.display.update()

def show_results(round_data):
    running = True
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 40)

    while running:
        screen.blit(background, (0, 0))

        title_text = title_font.render("Your results:", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 30))

        congrats1 = title_font.render("Congratulations!", True, (0, 0, 0))
        congrats2 = title_font.render("You can also try other levels!", True, (0, 0, 0))
        screen.blit(congrats1, (WIDTH / 2 - congrats1.get_width() / 2, 300))
        screen.blit(congrats2, (WIDTH / 2 - congrats2.get_width() / 2, 330))

        headers = ["Word of round:", "Difficulty:", "Found words:", "Total score:"]
        for i, header in enumerate(headers):
            text = font.render(header, True, (0, 0, 0))
            screen.blit(text, (100 + i * 200, 80))

        pygame.draw.line(screen, (0, 0, 0), (80, 110), (WIDTH - 80, 110), 2)

        for idx, entry in enumerate(round_data[-10:]):
            word, mode, found_count, score = entry
            row_y = 120 + idx * 35

            row_data = [word, mode, str(found_count), str(score)]
            for i, data in enumerate(row_data):
                text = font.render(data, True, (0, 0, 0))
                screen.blit(text, (100 + i * 200, row_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == menu_back:
                main_menu()

            menu_back.handle_event(event)

        menu_back.check_hover(pygame.mouse.get_pos())
        menu_back.draw(screen)

        pygame.display.flip()

def show_score():
    running = True
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 40)

    while running:
        screen.blit(background, (0, 0))

        title_text = title_font.render("Score Table", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 30))

        headers = ["Word of round:", "Difficulty:", "Found words:", "Total score:"]
        for i, header in enumerate(headers):
            text = font.render(header, True, (0, 0, 0))
            screen.blit(text, (100 + i * 200, 80))

        pygame.draw.line(screen, (0, 0, 0), (80, 110), (WIDTH - 80, 110), 2)

        for idx, entry in enumerate(score_table[-10:]):
            word, mode, found_count, score = entry
            row_y = 120 + idx * 35

            row_data = [word, mode, str(found_count), str(score)]
            for i, data in enumerate(row_data):
                text = font.render(data, True, (0, 0, 0))
                screen.blit(text, (100 + i * 200, row_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == menu_back:
                main_menu()

            menu_back.handle_event(event)

        menu_back.check_hover(pygame.mouse.get_pos())
        menu_back.draw(screen)

        pygame.display.flip()

main_menu()
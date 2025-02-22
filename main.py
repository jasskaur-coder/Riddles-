import pygame
import random
import textwrap
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Solve the Riddle! 🧩")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 69, 58)
GREEN = (50, 205, 50)
GREY = (128, 128, 128)

font = pygame.font.Font(None, 40)
large_font = pygame.font.Font(None, 55)

with open("riddles.txt", "r", encoding="utf-8") as f:
    riddles = [line.strip().split("|") for line in f]

try:
    with open("leaderboard.json", "r") as f:
        leaderboard = json.load(f)
except FileNotFoundError:
    leaderboard = {}
def normalize_text(text):
    return text.strip().lower().replace("’", "'").replace("“", "\"").replace("”", "\"")
def save_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)
def new_round():
    global current_riddle, correct_answer, user_guess, start_time, emoji_to_display, particles
    current_riddle, correct_answer = random.choice(riddles)
    correct_answer = normalize_text(correct_answer)
    user_guess = ""
    start_time = pygame.time.get_ticks()
    emoji_to_display = None
    particles = []  

def draw_background():
    for y in range(HEIGHT):
        color = (y // 3, y // 3, y // 3)  
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
def draw_wrapped_text(text, font, color, x, y, max_width):
    lines = textwrap.wrap(text, width=40)
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * 40))

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(20, 40)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)

user_guess = ""
current_riddle = ""
correct_answer = ""
score = 0
particles = []
new_round()

game_running = True
TIMER_LIMIT = 20000  

happy_emoji = pygame.image.load("happy.png")
sad_emoji = pygame.image.load("sad.png")
happy_emoji = pygame.transform.scale(happy_emoji, (100, 100))
sad_emoji = pygame.transform.scale(sad_emoji, (100, 100))
emoji_to_display = None

while game_running:
    draw_background()
    
    title_text = large_font.render("🧠 Solve the Riddle! 🧠", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 40))
    
    draw_wrapped_text(current_riddle, font, GREY, 50, 150, WIDTH - 100)
    
    input_text = font.render("Your Answer: " + user_guess, True, GREEN)
    screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, 300))
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 50))
    
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, (TIMER_LIMIT - elapsed_time) // 1000)
    timer_text = font.render(f"⏳ Time Left: {remaining_time}s", True, RED)
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 100))
    
    bar_width = max(0, (TIMER_LIMIT - elapsed_time) / TIMER_LIMIT * (WIDTH - 100))
    bar_color = RED if remaining_time <= 3 else GREEN
    pygame.draw.rect(screen, bar_color, (50, 550, bar_width, 20))
    
    if emoji_to_display:
        screen.blit(emoji_to_display, (WIDTH // 2 - 50, 400))
    
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.life <= 0:
            particles.remove(particle)
    
    if elapsed_time > TIMER_LIMIT:
        result_text = font.render(f"⌛ Time's up! The answer was: {correct_answer}", True, RED)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 450))
        emoji_to_display = sad_emoji
        pygame.display.flip()
        pygame.time.delay(2000)
        new_round()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check answer
                if normalize_text(user_guess) == correct_answer:
                    result_text = font.render("✅ Correct! 🎉", True, GREEN)
                    emoji_to_display = happy_emoji
                    score += 10
                    for _ in range(20):
                        particles.append(Particle(WIDTH // 2, 400))
                else:
                    result_text = font.render(f"❌ Wrong! The answer was: {correct_answer}", True, RED)
                    emoji_to_display = sad_emoji
                    score -= 5
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 450))
                pygame.display.flip()
                pygame.time.delay(2000)
                new_round()
            elif event.key == pygame.K_BACKSPACE:
                user_guess = user_guess[:-1]
            else:
                user_guess += event.unicode
    
    pygame.display.flip()
    
pygame.quit()

player_name = input("Enter your name: ")
leaderboard[player_name] = max(score, leaderboard.get(player_name, 0))
save_leaderboard()
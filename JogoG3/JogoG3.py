#Trabalho final - Jogo 2D em Pygame
#Personagem pula com a tecla "espaço"
#Para vencer o jogo precisa conseguir 20 pontos

import pygame
from sys import exit
from random import randint, choice
import math

# Classe do personagem

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        andar1 = pygame.image.load('graphics/player/andar1.png').convert_alpha()
        andar2 = pygame.image.load('graphics/player/andar2.png').convert_alpha()
        self.player_walk = [andar1, andar2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/pular.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        # Áudio de pulo
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def reset_position(self):
        self.rect.midbottom = (80, 300)
        self.gravity = 0


# Classe dos obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            if type == "snail":
                lesma1 = pygame.image.load('graphics/snail/lesma1.png').convert_alpha()
                lesma2 = pygame.image.load('graphics/snail/lesma2.png').convert_alpha()
                self.frames = [lesma1, lesma2]
                y_pos = 300
            else:
                evil1 = pygame.image.load('graphics/EvilPlayer/andar1.png').convert_alpha()
                evil2 = pygame.image.load('graphics/EvilPlayer/andar2.png').convert_alpha()
                self.frames = [evil1, evil2]
                y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Função para exibir a pontuação
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'pontos: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Função para verificar colisões
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# Função para exibir a mensagem de Game Over
def show_game_over_message():
    game_over_message = test_font.render('GAME OVER', False, (196, 111, 138))
    game_over_rect = game_over_message.get_rect(center=(400, 320))
    screen.blit(game_over_message, game_over_rect)
    score_message = test_font.render(f'pontos acumulados: {score}', False, (255, 255, 255))
    score_rect = score_message.get_rect(center=(400, 350))
    screen.blit(score_message, score_rect)
    message_victory = test_font.render('aperte espaço para reiniciar', False, (255, 255, 255))
    message_victory_rect = message_victory.get_rect(center=(400, 380))


# Função para exibir a mensagem de Vitória
def show_victory_message():
    victory_message = test_font.render('VOCE VENCEU!', False, (0, 255, 0))
    victory_rect = victory_message.get_rect(center=(400, 350))
    screen.blit(victory_message, victory_rect)


# Função para reiniciar o jogo
def restart_game():
    global game_active, game_over, victory, start_time, score
    game_active = True
    game_over = False
    victory = False
    start_time = int(pygame.time.get_ticks() / 1000)
    score = 0
    player.sprite.reset_position()
    obstacle_group.empty()


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
game_over = False
victory = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_width = sky_surface.get_width()
sky_tiles = math.ceil(800 / sky_width) + 1
scroll_s = 0

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_width = ground_surface.get_width()
ground_tiles = math.ceil(400 / ground_width) + 1
scroll_g = 0

parado = pygame.image.load('graphics/player/parado.png').convert_alpha()
parado = pygame.transform.rotozoom(parado, 0, 2)
parado_rect = parado.get_rect(center=(400, 200))

game_name = test_font.render('runners night', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('aperte espaco para iniciar', False, (255, 255, 255))
game_message_rect = game_message.get_rect(center=(400, 330))

message_victory = test_font.render('aperte espaco para reiniciar', False, (255, 255, 255))
message_victory_rect = message_victory.get_rect(center=(400, 380))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','evil'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_over or victory:
                    restart_game()
                else:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        for el in range (0,sky_tiles):
            screen.blit(sky_surface,(el * sky_width + scroll_s,0))
        scroll_s -= 1
        if abs(scroll_s) > sky_width:
            scroll_s = 0
        for el in range (0, ground_tiles):
            screen.blit(ground_surface,(el * ground_width + scroll_g , 300))
        scroll_g -= 4
        if abs(scroll_g) > ground_width:
            scroll_g = 0

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

        if score == 20:
            game_active = False
            victory = True

        if not game_active and not game_over and not victory:
            game_over = True

    else:
        screen.fill((51, 51, 51))
        screen.blit(parado, parado_rect)

        screen.blit(game_name, game_name_rect)

        if game_over:
            show_game_over_message()
            screen.blit(message_victory, message_victory_rect)
        elif victory:
            show_victory_message()
            screen.blit(message_victory, message_victory_rect)
        else:
            screen.blit(game_message, message_victory_rect)

    pygame.display.update()
    clock.tick(60)

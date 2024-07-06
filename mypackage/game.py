from .utilities import ImageHandler, SFXHandler
import pygame
pygame.font.init()

PLAYER_1_HIT = pygame.USEREVENT + 1
PLAYER_2_HIT = pygame.USEREVENT + 2


class GameBoard(ImageHandler):
    def __init__(self, w, h, p1, p2) -> None:
        super().__init__()
        self.width = w
        self.height = h
        self.fps = 60
        # Overide ImageHandler attributes
        self.ship_size = (self.width * 0.1, self.width * 0.1)
        self.screen_size = (self.width, self.height)
        self.colors = {"border": "#4779c4", "health_font": "white", "winner_font": "white"}
        self.player_1 = p1
        self.player_2 = p2
        self.health_font = pygame.font.SysFont("timesnewroman", int(self.width * 0.05))
        self.winner_font = pygame.font.SysFont("timesnewroman", int(self.width * 0.08))

    def render_game(self, surface):
        """Renders all game elements"""
        self.render_background(surface)
        self.render_border(surface)
        self.render_score_details(surface)
        self.player_1.draw(surface)
        self.player_2.draw(surface)
        self.render_winner(surface)

    def render_background(self, surface):
        """Renders background image"""
        surface.blit(self.get_background(), (0,0))

    def render_border(self, surface):
        """Renders a full height rectangle at center of screen"""
        size = (self.width * 0.005, self.height)
        pos = (self.width * 0.5 + (size[0] // 2), 0)
        pygame.draw.rect(surface, self.colors["border"], [pos, size])

    def render_score_details(self, surface):
        """Renders the health values of both players"""
        player_1_health = self.health_font.render(f"Health: {self.player_1.health}", 1,self.colors["health_font"])
        player_2_health = self.health_font.render(f"Health: {self.player_2.health}", 1,self.colors["health_font"])

        surface.blit(player_1_health, (0,0))
        surface.blit(player_2_health, ((self.width - player_2_health.get_width()),0))


    def render_winner(self, surface):
        winner = self.check_winner()
        if winner:
            winner_text = self.winner_font.render(f"{winner}", 1, self.colors["winner_font"])
            surface.blit(winner_text, ((self.width * 0.5) - (winner_text.get_width() // 2), (self.height * 0.5) - (winner_text.get_height() // 2)))
            
    def check_winner(self):
        """Returns winner"""
        if self.player_1.health == 0:
            return "Player 2 Wins"
        elif self.player_2.health == 0:
            return "Player 1 Wins"

            


class Player(ImageHandler, SFXHandler):
    def __init__(self, w: int, h: int, ship_type: int, player: str, x: int) -> None:
        ImageHandler.__init__(self)
        SFXHandler.__init__(self)
        """Inializes Player Details and Controls"""
        self.w = w
        self.h = h
        self.player = player
        self.image = self.choose_ship(ship_type)
        self.p_width = w * 0.1
        self.p_height = w * 0.1
        self.ship_size = (self.p_width, self.p_height) # Overide parent attribute
        self.rect = self.image.get_rect()
        self.rect.center = (x, (h // 2))
        self.speed = 6
        self.health = 10

        self.ball_size = (w * 0.02, w * 0.02) # Overide parent attribute
        self.energy_ball_image = self.get_energy_ball() 
        self.ball_speed = 4
        self.energy_balls_list:list = []
        self.energy_ball_cooldown = 0
        self.max_cooldown = 20



    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.handle_energy_balls(surface)
    def update(self, key, surface):
        """Updates all player details including ship and bullet position and status"""

        # Decrement cooldown
        if self.energy_ball_cooldown > 0:
            self.energy_ball_cooldown -= 1
        
        # Check energy ball status
        self.validate_energy_balls()


        if self.player == "p1":
            # Initialize Bounds
            r_bnd = self.w * 0.5
            l_bnd = 0
            u_bnd = 0
            d_bnd = self.h

            # Handle Ship movement
            if key[pygame.K_w] and self.rect.y > u_bnd:
                self.move_up()
            if key[pygame.K_s] and self.rect.y + self.rect.height < d_bnd:
                self.move_down()
            if key[pygame.K_a] and self.rect.x > l_bnd:
                self.move_left()
            if key[pygame.K_d] and self.rect.x + self.rect.width < r_bnd:
                self.move_right()

            # Handle player 1'senergy ball movement
            if key[pygame.K_SPACE] and self.energy_ball_cooldown == 0:
                self.add_energy_balls()
                self.play_energy_ball_sound()
                self.energy_ball_cooldown = self.max_cooldown

        if self.player == "p2":
            # Initialize Bounds
            r_bnd = self.w 
            l_bnd = self.w * 0.5
            u_bnd = 0
            d_bnd = self.h

            # Hanlde player 2's ship Movement
            if key[pygame.K_UP] and self.rect.y > u_bnd:
                self.move_up()
            if key[pygame.K_DOWN] and self.rect.y < l_bnd:
                self.move_down()
            if key[pygame.K_LEFT] and self.rect.x > l_bnd:
                self.move_left()
            if key[pygame.K_RIGHT] and self.rect.x + self.rect.width < r_bnd:
                self.move_right()

            # Hanlde player 2's energy ball movement
            if key[pygame.K_RSHIFT] and self.energy_ball_cooldown == 0:
                self.add_energy_balls()
                self.play_energy_ball_sound()
                self.energy_ball_cooldown = self.max_cooldown

    def validate_energy_balls(self):
        """Iterates through list of energy ball bullets and removes balls them from list if they
        are out of bound"""
        i = 0
        while i < len(self.energy_balls_list):
            ball = self.energy_balls_list[i]
            ball_rect = ball["ball_rect"]
            ball_player = ball["player"]

            if ball_player == "p1" and ball_rect.x > self.w:
                self.energy_balls_list.remove(ball)
            elif ball_player == "p2" and ball_rect.x < 0:
                self.energy_balls_list.remove(ball)
            else:
                i += 1  # Only increment if no removal to avoid skipping elemen
    
    def check_bullet_collision(self, enemy_player):
        """Envokes hit event if bullet has collided with player"""
        for ball in self.energy_balls_list:
            if ball["ball_rect"].colliderect(enemy_player):
                if ball["player"] == "p1":
                    pygame.event.post(pygame.event.Event(PLAYER_2_HIT))
                elif ball["player"] == "p2":
                    pygame.event.post(pygame.event.Event(PLAYER_1_HIT))
                self.energy_balls_list.remove(ball)
            
    def handle_collision_event(self, event):
        """Checks if player his event has been envoked"""
        if self.player == "p1":
            if event.type == PLAYER_1_HIT:
                self.health -= 1
                self.play_ship_hit_sound()
        elif self.player == "p2":
            if event.type == PLAYER_2_HIT:
                self.health -= 1
                self.play_ship_hit_sound()


    def add_energy_balls(self):
        """Manages energy balls list"""
        if len(self.energy_balls_list) < 3:
            ball_img = self.energy_ball_image
            rect = ball_img.get_rect()
            rect.center = self.rect.center
            data = {
                "ball_image": ball_img,
                "ball_rect": rect,
                "player": self.player
            }
            self.energy_balls_list.append(data)


    def handle_energy_balls(self, surface):
        """Controls position and rendering of balls"""
        for ball in self.energy_balls_list:
            surface.blit(ball["ball_image"], ball["ball_rect"])
            if ball["player"] == "p1":
                ball["ball_rect"].x += self.ball_speed
            elif ball["player"] == "p2":
                ball["ball_rect"].x -= self.ball_speed


    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed


    def choose_ship(self, ship_type):
        if self.player == "p1":
            degree = 270
        elif self.player == "p2":
            degree = 90
        if ship_type == 1:
            return self.get_ship_1(degree)
        if ship_type == 2:
            return self.get_ship_2(degree)
        if ship_type == 3:
            return self.get_ship_3(degree)
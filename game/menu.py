import random
import sys

import pygame

import game
from scripts import button
from scripts import slider
from scripts import sprite_sheet as ss


class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('Sounds/menu_music.mp3')

        # screen
        screen_width = 1280
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Dorock')

        # FPS
        clock = pygame.time.Clock()
        fps = 60

        # define fonts
        pixel_50 = pygame.font.Font('Fonts/pixel.ttf', 50)

        # define color
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)

        # music
        pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=-1, fade_ms=5000)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.pause()

        # sounds
        sound_hover = pygame.mixer.Sound('Sounds/hover_button_sound.ogg')
        sound_hover.set_volume(0.15)

        def draw_text(text, font, text_color, x, y):
            wtext = font.render(text, False, text_color)
            screen.blit(wtext, (x, y))

        def draw_fade_text(text, font, text_color, x, y, fade_speed=1, increasing=True, alpha=0, circles=0):
            if increasing:
                alpha += fade_speed
                if alpha >= 255:
                    alpha = 255
                    increasing = False
            else:
                alpha -= fade_speed
                if alpha <= 0:
                    alpha = 0
                    increasing = True
                    circles += 1

            fade_text = font.render(text, True, text_color)
            fade_text.set_alpha(alpha)

            text_rect = fade_text.get_rect(center=(x, y))

            screen.blit(fade_text, text_rect)

            pygame.display.update()
            pygame.time.delay(20)

            return increasing, alpha, circles

        def main_menu(fresh_start, started_time=pygame.time.get_ticks(), turn_on_first_time=True, vol=0.5):
            running = True

            # game variables
            game_started = fresh_start
            increasing = True
            alpha = 0
            circles = 2

            start_hovered = False
            settings_hovered = False
            exit_hovered = False

            # loading images for menu
            bg_img = pygame.image.load('Images/bg_menu.jpg').convert_alpha()
            bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
            start_img = pygame.image.load('Images/sign_play.png').convert_alpha()
            start_img_bright = pygame.image.load('Images/sign_play_bright.png').convert_alpha()
            settings_img = pygame.image.load('Images/sign_settings.png').convert_alpha()
            settings_img_bright = pygame.image.load('Images/sign_settings_bright.png').convert_alpha()
            exit_img = pygame.image.load('Images/sign_exit.png').convert_alpha()
            exit_img_bright = pygame.image.load('Images/sign_exit_bright.png').convert_alpha()

            # making them buttons
            start_button = button.Button(465, 50, start_img, 0.15)
            start_button_bright = button.Button(465, 50, start_img_bright, 0.15)
            settings_button = button.Button(465, 230, settings_img, 0.15)
            settings_button_bright = button.Button(465, 230, settings_img_bright, 0.15)
            exit_button = button.Button(465, 410, exit_img, 0.15)
            exit_button_bright = button.Button(465, 410, exit_img_bright, 0.15)

            # birds
            bird_sheet_image = pygame.image.load('Images/bird_sprites.png').convert_alpha()
            bird_sprites = ss.SpriteSheet(bird_sheet_image)

            # birds parameters
            bird_width, bird_height = 160, 160
            bird_scale = 0.5

            bird_x = 1280
            bird_y = random.randint(0, 300)
            last_bird = pygame.time.get_ticks()

            # creating birds list
            bird_list = []
            animations = 8
            last_update = pygame.time.get_ticks()
            animation_cd = 100
            frame = 0

            for frame in range(animations):
                bird_list.append(bird_sprites.get_image(frame, bird_width, bird_height, bird_scale, black_color))

            while running:
                screen.fill(black_color)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not game_started:
                            game_started = True
                            alpha = 0
                            increasing = True
                            circles = 0

                    if event.type == pygame.QUIT:
                        running = False

                # check if game is started
                if game_started:
                    if circles == 0:
                        increasing, alpha, circles = draw_fade_text("\"The Procrastinators\" presents", pixel_50,
                                                                    white_color, 640, 360, 100, increasing, alpha,
                                                                    circles)
                    elif circles == 1:
                        increasing, alpha, circles = draw_fade_text("Dorock", pixel_50, (179, 0, 0), 640, 360, 100,
                                                                    increasing, alpha, circles)
                    else:
                        screen.blit(bg_img, (0, 0))
                        current_time = pygame.time.get_ticks()
                        if start_button.draw(screen, 'hover'):
                            if start_button_bright.draw(screen) and current_time - started_time > 600:
                                svol = 1 if (sound_hover.get_volume() > 0) else 0
                                game.Game(self, svol, vol).run()
                                running = False
                            if not start_hovered:
                                pygame.mixer.Sound.play(sound_hover)
                                start_hovered = True
                        else:
                            start_button.draw(screen)
                            start_hovered = False

                        if settings_button.draw(screen, 'hover'):
                            if settings_button_bright.draw(screen) and current_time - started_time > 600:
                                running = False
                                settings_menu(current_time, vol)
                            if not settings_hovered:
                                pygame.mixer.Sound.play(sound_hover)
                                settings_hovered = True
                        else:
                            settings_button.draw(screen)
                            settings_hovered = False

                        if exit_button.draw(screen, 'hover'):
                            if exit_button_bright.draw(screen) and current_time - started_time > 600:
                                pygame.quit()
                                sys.exit()
                            if not exit_hovered:
                                sound_hover.play(0, 0, fade_ms=0)
                                exit_hovered = True
                        else:
                            exit_button.draw(screen)
                            exit_hovered = False

                        if not turn_on_first_time:
                            pygame.mixer.music.unpause()
                            turn_on_first_time = True
                            vol = pygame.mixer.music.get_volume()

                        # update animation

                        if current_time - last_update >= animation_cd:
                            if frame == animations - 1:
                                frame = 0
                            else:
                                frame += 1
                            last_update = current_time

                        if bird_x > 0:
                            bird_x -= random.randint(3, 10)
                            screen.blit(bird_list[frame], (bird_x, bird_y))
                        else:
                            if current_time - last_bird > random.randint(4000, 30000):
                                bird_x = 1280
                                bird_y = random.randint(0, 300)
                                screen.blit(bird_list[frame], (bird_x, bird_y))
                                animation_cd = random.randint(50, 150)
                                last_bird = current_time

                else:
                    increasing, alpha, circles = draw_fade_text("Press SPACE to start the game", pixel_50, white_color,
                                                                640, 360, 10, increasing, alpha, circles)
                pygame.display.update()

                clock.tick(fps)

        def settings_menu(started_time, vol):
            # image stuff for settings menu
            settings_bg = pygame.image.load('Images/settings_bg.png').convert_alpha()
            settings_bg = pygame.transform.scale(settings_bg, (screen_width, screen_height))
            audio_img = pygame.image.load('Images/audio_sign.png').convert_alpha()
            audio_img_bright = pygame.image.load('Images/audio_bright_sign.png').convert_alpha()
            video_img = pygame.image.load('Images/video_sign.png').convert_alpha()
            video_img_bright = pygame.image.load('Images/video_bright_sign.png').convert_alpha()
            back_img = pygame.image.load('Images/back.png').convert_alpha()
            back_img_bright = pygame.image.load('Images/back_bright.png').convert_alpha()

            # making buttons
            audio_button = button.Button(465, 160, audio_img, 0.15)
            audio_button_bright = button.Button(465, 160, audio_img_bright, 0.15)
            video_button = button.Button(465, 340, video_img, 0.15)
            video_button_bright = button.Button(465, 340, video_img_bright, 0.15)
            back_button = button.Button(350, 75, back_img, 0.4)
            back_button_bright = button.Button(350, 75, back_img_bright, 0.4)

            # sounds
            audio_hovered = False
            video_hovered = False
            back_hovered = False

            running = True
            while running:
                screen.fill(black_color)
                screen.blit(settings_bg, (0, 0))
                current_time = pygame.time.get_ticks()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            main_menu(True, current_time, vol=vol)

                if audio_button.draw(screen, 'hover'):
                    if audio_button_bright.draw(screen) and current_time - started_time > 600:
                        running = False
                        audio_menu(current_time, vol)
                    if not audio_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        audio_hovered = True
                else:
                    audio_button.draw(screen)
                    audio_hovered = False

                if video_button.draw(screen, 'hover'):
                    if video_button_bright.draw(screen) and current_time - started_time > 600:
                        video_menu(current_time)
                    if not video_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        video_hovered = True
                else:
                    video_button.draw(screen)
                    video_hovered = False

                if back_button.draw(screen, 'hover'):
                    if back_button_bright.draw(screen) and current_time - started_time > 600:
                        running = False
                        main_menu(True, current_time, vol=vol)
                    if not back_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        back_hovered = True
                else:
                    back_button.draw(screen)
                    back_hovered = False

                pygame.display.update()
                clock.tick(fps)

        def audio_menu(started_time, vol):

            # images
            audio_bg_img = pygame.image.load('Images/AudioMenu/audio_bg.png').convert_alpha()
            audio_bg = pygame.transform.scale(audio_bg_img, (screen_width, screen_height))

            music_off_img = pygame.image.load('Images/AudioMenu/music_off.png').convert_alpha()
            music_on_img = pygame.image.load('Images/AudioMenu/music_on.png').convert_alpha()
            effects_off_img = pygame.image.load('Images/AudioMenu/effects_off.png').convert_alpha()
            effects_on_img = pygame.image.load('Images/AudioMenu/effects_on.png').convert_alpha()
            bg_slider = pygame.image.load('Images/AudioMenu/bg_slider.png').convert_alpha()
            bg_slider = pygame.transform.scale(bg_slider,
                                               (bg_slider.get_width() * 0.4654, bg_slider.get_height() * 0.4657))
            sounds_slider = pygame.image.load('Images/AudioMenu/sounds_slider.png').convert_alpha()
            sounds_slider = pygame.transform.scale(sounds_slider, (sounds_slider.get_width()*0.4654,
                                                                   sounds_slider.get_height()*0.4657))
            back_img = pygame.image.load('Images/back.png').convert_alpha()
            back_img_bright = pygame.image.load('Images/back_bright.png').convert_alpha()

            # buttons
            music_on = button.Button(227, 245, music_on_img)
            music_off = button.Button(227, 245, music_off_img)
            sounds_on = button.Button(227, 347, effects_on_img)
            sounds_off = button.Button(227, 347, effects_off_img)
            back_button = button.Button(350, 75, back_img, 0.4)
            back_button_bright = button.Button(350, 75, back_img_bright, 0.4)

            music_hovered = False
            sounds_hovered = False
            back_hovered = False

            # SLIDER
            test_slider = slider.Slider(772, 283, 253, 2, screen, vol)

            running = True
            while running:
                screen.fill(black_color)
                screen.blit(audio_bg, (0, 0))
                current_time = pygame.time.get_ticks()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            settings_menu(current_time, vol)
                    if event.type == pygame.MOUSEMOTION:
                        if pygame.mouse.get_pressed()[0] and test_slider.on_slider(pygame.mouse.get_pos()[0],
                                                                                   pygame.mouse.get_pos()[1]):
                            test_slider.handle_event(screen, pygame.mouse.get_pos()[0])
                            vol = test_slider.get_volume() / 100
                            pygame.mixer.music.set_volume(vol)

                if back_button.draw(screen, 'hover'):
                    if back_button_bright.draw(screen) and current_time - started_time > 600:
                        running = False
                        settings_menu(current_time, vol)
                    if not back_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        back_hovered = True
                else:
                    back_button.draw(screen)
                    back_hovered = False

                if music_off.draw(screen, 'hover'):
                    music_on.draw(screen)
                    if not music_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        music_hovered = True
                else:
                    music_off.draw(screen)
                    music_hovered = False
                test_slider.draw(screen, vol)

                svol = sound_hover.get_volume()
                if sounds_off.draw(screen, 'hover'):
                    if sounds_on.draw(screen):
                        if svol == 0:
                            sound_hover.set_volume(0.15)
                        else:
                            sound_hover.set_volume(0)
                    if not sounds_hovered:
                        pygame.mixer.Sound.play(sound_hover)
                        sounds_hovered = True
                else:
                    sounds_off.draw(screen)
                    sounds_hovered = False

                if svol == 0:
                    draw_text('OFF', pixel_50, (44, 27, 9), 856, 356)
                else:
                    draw_text('ON', pixel_50, (44, 27, 9), 868, 356)

                screen.blit(bg_slider, (729, 257))
                screen.blit(sounds_slider, (727, 362))

                pygame.display.update()
                clock.tick(fps)

        def video_menu(started_time):
            video_bg_img = pygame.image.load('Images/audio_bg.png').convert_alpha()
            video_bg = pygame.transform.scale(video_bg_img, (screen_width, screen_height))

        main_menu(self, False, turn_on_first_time=False)

        pygame.quit()
        sys.exit()


Menu()
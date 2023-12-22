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

        resolutions = ['720x576', '1280x720', 'FULL HD']

        # FPS
        clock = pygame.time.Clock()
        fps = 60

        # define fonts
        pixel_50 = pygame.font.Font('Fonts/pixel.ttf', 50)

        # define color
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)
        settings_color = (44, 27, 9)

        # music
        pygame.mixer.init()
        pygame.mixer.music.play(loops=-1, fade_ms=5000)
        pygame.mixer.music.set_volume(0.5)

        # sounds
        sound_hover = pygame.mixer.Sound('Sounds/hover_button_sound.ogg')
        sound_hover.set_volume(0.15)

        back_img = pygame.image.load('Images/Buttons/back.png').convert_alpha()
        back_img_bright = pygame.image.load('Images/Buttons/back_bright.png').convert_alpha()
        back_button = button.Button(350, 75, back_img, 0.4)
        back_button_bright = button.Button(350, 75, back_img_bright, 0.4)

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

        def button_actions(cbutton, cbutton_b, cur_time, start_time, ishovered):
            action = False
            if cbutton.draw(screen, 'hover'):
                if cbutton_b.draw(screen) and cur_time - start_time > 400:
                    action = True
                if not ishovered:
                    pygame.mixer.Sound.play(sound_hover)
                    ishovered = True
            else:
                cbutton.draw(screen)
                ishovered = False

            return action, ishovered

        def main_menu(fresh_start, started_time=pygame.time.get_ticks(), vol=0.5):
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
            start_img = pygame.image.load('Images/Buttons/sign_play.png').convert_alpha()
            start_img_bright = pygame.image.load('Images/Buttons/sign_play_bright.png').convert_alpha()
            settings_img = pygame.image.load('Images/Buttons/sign_settings.png').convert_alpha()
            settings_img_bright = pygame.image.load('Images/Buttons/sign_settings_bright.png').convert_alpha()
            exit_img = pygame.image.load('Images/Buttons/sign_exit.png').convert_alpha()
            exit_img_bright = pygame.image.load('Images/Buttons/sign_exit_bright.png').convert_alpha()

            # making them buttons
            start_button = button.Button(465, 50, start_img, 0.15)
            start_button_bright = button.Button(465, 50, start_img_bright, 0.15)
            settings_button = button.Button(465, 230, settings_img, 0.15)
            settings_button_bright = button.Button(465, 230, settings_img_bright, 0.15)
            exit_button = button.Button(465, 410, exit_img, 0.15)
            exit_button_bright = button.Button(465, 410, exit_img_bright, 0.15)

            # birds and axolotl
            bird_sheet_image = pygame.image.load('Images/bird_sprites.png').convert_alpha()
            bird_sprites = ss.SpriteSheet(bird_sheet_image)
            axolotl_sheet_image = pygame.image.load('Images/axolotl_sprites.png').convert_alpha()
            axolotl_sprites = ss.SpriteSheet(axolotl_sheet_image)

            # birds and axolotl parameters
            bird_width, bird_height = 160, 160
            bird_scale = 0.5
            axolotl_width, axolotl_height = 1373, 1373
            axolotl_scale = 0.1

            bird_x, bird_y = 1280, random.randint(0, 300)
            last_bird = pygame.time.get_ticks()

            axolotl_x, axolotl_y = 500, 600

            # creating birds and axolotl list
            bird_list = []
            animations = 8
            last_update = pygame.time.get_ticks()
            animation_cd = 100
            frame = 0

            axolotl_list = []
            axo_animations = 10
            axolotl_frame = 0

            for frame in range(animations):
                bird_list.append(bird_sprites.get_image(frame, bird_width, bird_height, bird_scale, black_color))

            for axolotl_frame in range(axo_animations):
                axolotl_list.append((axolotl_sprites.get_image(axolotl_frame, axolotl_width, axolotl_height, axolotl_scale,
                                                               black_color)))


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

                        start_action, start_hovered = button_actions(start_button, start_button_bright, current_time,
                                                                     started_time, start_hovered)

                        if start_action:
                            svol = 1 if (sound_hover.get_volume() > 0) else 0
                            game.Game(self, svol, vol).run()
                            running = False

                        settings_action, settings_hovered = button_actions(settings_button, settings_button_bright,
                                                                           current_time, started_time, settings_hovered)
                        if settings_action:
                            settings_menu(current_time, vol)
                            running = False

                        exit_action, exit_hovered = button_actions(exit_button, exit_button_bright, current_time,
                                                                   started_time, exit_hovered)
                        if exit_action:
                            pygame.quit()
                            sys.exit()

                        # update animation
                        if current_time - last_update >= animation_cd:
                            if frame == animations - 1:
                                frame = 0
                            else:
                                frame += 1

                            if axolotl_frame == axo_animations - 1:
                                axolotl_frame = 0
                            else:
                                axolotl_frame += 1
                            last_update = current_time

                        if bird_x > 0:
                            bird_x -= random.randint(3, 10)
                            screen.blit(bird_list[frame], (bird_x, bird_y))
                        else:
                            if current_time - last_bird > random.randint(4000, 30000):
                                bird_x = 1280
                                bird_y = random.randint(0, 300)
                                screen.blit(bird_list[frame], (bird_x, bird_y))
                                last_bird = current_time

                        screen.blit(axolotl_list[axolotl_frame], (axolotl_x, axolotl_y))
                else:
                    increasing, alpha, circles = draw_fade_text("Press SPACE to start the game", pixel_50, white_color,
                                                                640, 360, 10, increasing, alpha, circles)
                pygame.display.update()

                clock.tick(fps)

        def settings_menu(started_time, vol=pygame.mixer.music.get_volume()):
            # image stuff for settings menu
            settings_bg = pygame.image.load('Images/settings_bg.png').convert_alpha()
            settings_bg = pygame.transform.scale(settings_bg, (screen_width, screen_height))
            audio_img = pygame.image.load('Images/Buttons/audio_sign.png').convert_alpha()
            audio_img_bright = pygame.image.load('Images/Buttons/audio_bright_sign.png').convert_alpha()
            video_img = pygame.image.load('Images/Buttons/video_sign.png').convert_alpha()
            video_img_bright = pygame.image.load('Images/Buttons/video_bright_sign.png').convert_alpha()

            # making buttons
            audio_button = button.Button(465, 160, audio_img, 0.15)
            audio_button_bright = button.Button(465, 160, audio_img_bright, 0.15)
            video_button = button.Button(465, 340, video_img, 0.15)
            video_button_bright = button.Button(465, 340, video_img_bright, 0.15)

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

                audio_action, audio_hovered = button_actions(audio_button, audio_button_bright, current_time,
                                                             started_time, audio_hovered)
                if audio_action:
                    audio_menu(current_time, vol)
                    running = False

                video_action, video_hovered = button_actions(video_button, video_button_bright, current_time,
                                                             started_time, video_hovered)
                if video_action:
                    video_menu(current_time)
                    running = False

                back_action, back_hovered = button_actions(back_button, back_button_bright, current_time, started_time,
                                                           back_hovered)
                if back_action:
                    main_menu(True, current_time, vol=vol)
                    running = False

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

            # buttons
            music_on = button.Button(227, 245, music_on_img)
            music_off = button.Button(227, 245, music_off_img)
            sounds_on = button.Button(227, 347, effects_on_img)
            sounds_off = button.Button(227, 347, effects_off_img)

            music_hovered = False
            sounds_hovered = False
            back_hovered = False

            # SLIDER
            test_slider = slider.Slider(772, 282, 253, 2, screen, vol)

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

                back_action, back_hovered = button_actions(back_button, back_button_bright, current_time, started_time,
                                                           back_hovered)
                if back_action:
                    settings_menu(current_time, vol)
                    running = False

                music_action, music_hovered = button_actions(music_off, music_on, current_time, started_time,
                                                             music_hovered)
                screen.blit(bg_slider, (729, 257))
                test_slider.draw(screen)

                svol = sound_hover.get_volume()
                sounds_action, sounds_hovered = button_actions(sounds_off, sounds_on, current_time, started_time,
                                                               sounds_hovered)
                if sounds_action:
                    if svol == 0:
                        sound_hover.set_volume(0.15)
                    else:
                        sound_hover.set_volume(0)

                if svol == 0:
                    draw_text('OFF', pixel_50, settings_color, 856, 356)
                else:
                    draw_text('ON', pixel_50, settings_color, 868, 356)

                screen.blit(sounds_slider, (727, 362))

                pygame.display.update()
                clock.tick(fps)

        def video_menu(started_time):

            # images
            video_bg_img = pygame.image.load('Images/VideoMenu/video_bg.png').convert_alpha()
            video_bg = pygame.transform.scale(video_bg_img, (screen_width, screen_height))
            resolution_on_img = pygame.image.load('Images/VideoMenu/resolution_on.png').convert_alpha()
            resolution_off_img = pygame.image.load('Images/VideoMenu/resolution_off.png').convert_alpha()
            resolution_slider = pygame.image.load('Images/VideoMenu/slider_resolution.png').convert_alpha()
            resolution_slider = pygame.transform.scale(resolution_slider, (resolution_slider.get_width() * 0.4654,
                                                                           resolution_slider.get_height() * 0.4657))
            # buttons
            resolution_on = button.Button(227, 245, resolution_on_img)
            resolution_off = button.Button(227, 245, resolution_off_img)

            back_hovered = False
            res_hovered = False

            running = True
            while running:
                screen.fill(black_color)
                screen.blit(video_bg, (0, 0))
                current_time = pygame.time.get_ticks()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            settings_menu(current_time)

                back_action, back_hovered = button_actions(back_button, back_button_bright, current_time, started_time,
                                                           back_hovered)
                if back_action:
                    settings_menu(current_time)
                    running = False

                res_action, res_hovered = button_actions(resolution_off, resolution_on, current_time, started_time,
                                                         res_hovered)
                if back_action:
                    settings_menu(current_time)
                    running = False

                draw_text('1280x720', pixel_50, settings_color, 783, 250)
                draw_text('Тут должно было быть что-то', pixel_50, settings_color, 260, 350)
                draw_text('функионирующее, но сложное.', pixel_50, settings_color, 260, 401)
                draw_text('Когда-нибудь будет', pixel_50, settings_color, 260, 470)

                screen.blit(resolution_slider, (729, 257))

                pygame.display.update()
                clock.tick(fps)

        main_menu(self, False)

        pygame.quit()
        sys.exit()


Menu()

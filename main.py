'''
cookie clicker project with pygame, chick as many times as you can to unlock new shit
has
clicks, level, user profiles (file savings with json)

'''
import pygame
import math
import json

import encryption
import base64
# import yaml
from user_class import *

#open data.json as read
with open('data.json', 'r') as file:
    data = json.load(file)
print(len(data), data)

#options yaml file, not being used
# with open('options.yaml', 'r') as file:
#     yaml = yaml.safe_load(file)
# print(yaml)


def main():
    # variables
    key = encryption.load_key()
    user_authenticate = False
    running = False
    user_profile = None
    print("Welcome to cookie clicker.")
    while True:
        global data, yaml
        print("""Options.
        1. Create a new profile
        2. Load old profile
        3. Exit
        """)
        user_option = int(input("What option? "))
        if user_option == 1:
            #create profile
            user_input_name = input("What is the name for the profile. ")
            user_input_password = input("Set a password. ")
            user_profile = Profile(user_input_name, 0, 1, 0)
            #encode in base64 so it can be saved in JSON
            password_encrypted = base64.b64encode(encryption.encrypt_msg(user_input_password, key)).decode("utf-8")
            new_data = {
                "name": user_input_name,
                "password": password_encrypted,
                "attributes": {"id": user_profile.get_random_id(), "level": 1, "cookies": 0}
            }
            with open('data.json', 'w') as file:
                data.append(new_data)
                json.dump(data, file, indent=4)
                print(len(data))
            print(f"User Profile {user_input_name} created! ID Number: {user_profile.get_random_id()}.")


        #load profile
        elif user_option == 2:
            user_input_load = input("Name of user to load?")
            with open('data.json', 'r') as file:
                data = json.load(file)
            for profile in data:
                if profile.get("name") == user_input_load:
                    #create object
                    user_profile = Profile(user_input_load, profile["attributes"]["id"], profile["attributes"]["level"],
                                           profile["attributes"]["cookies"])
                    while True:
                        user_input_password = input(f"Enter password for profile {user_profile.name}. ")
                        #decode base64 then decrypt with key
                        password_decrypted = base64.b64decode(profile.get("password"))
                        password_decrypted = encryption.decrypt_msg(password_decrypted, key)
                        if user_input_password == password_decrypted:
                            print("Object created using class 'Profile'", user_profile, "User auth: True")
                            print("User Authenticated, its you  clicking cookies!")
                            user_authenticate = True
                            break
                        else:
                            print("Incorrect Password, try again.")
                            continue
                    running = True
                    break
            if user_authenticate:
                break
            print("User not found.")
            #run second loop to start actual game
        else:
            print("Exit")
            break

    while user_authenticate and running:
        print(f"""------
    Starting Game...
    Cookie Clicker Version 1.0
    User: {user_profile}
    User-Authentication: {user_authenticate}
    Run-Time: {running}
    
    Current Cookies: {user_profile.get_cookie_clicks} (Each level resets cookie counter)
    Current Level: {user_profile.level} (Levels get exponentially harder by 2)
    ID/Name: {user_profile.id} {user_profile.name}
    
    Exit the screen or click x to save your stats.
    Click s to save your stats.
    
    Dependencies: Pygame{pygame.version.ver}
    
    Upcoming Updaters:
    - lifetime cookies
    - add a shop
------""")
        pygame.init()
        cookie_image = pygame.image.load("cookie.jpg")
        # initialize clock and screen objects
        screen_size = (1280, 720)
        screen = pygame.display.set_mode(screen_size)
        window = screen.get_rect() #gets double tuple (x1,y1), (x2,y2)
        pygame.display.set_caption("Cookie Clicker")
        font = pygame.font.Font(None, 30)
        clock = pygame.time.Clock()

        try:
            # You can draw the mole with this snippet:
            while running:
                screen.fill("light green")
                for event in pygame.event.get():

                    #events
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #distance formula to calculate how far from the circle
                        circle_distance = math.sqrt(
                            (event.pos[0] - screen_size[0]/2) ** 2 + (event.pos[1] - screen_size[1]/2) ** 2)
                        if circle_distance > 250: #n is circle radius
                            print("too far away")
                            continue

                        if user_profile.get_cookie_clicks >= user_profile.level ** 2:
                            print(user_profile.level_up())

                        user_profile.increment_cookie_clicks()
                        print("Current Cookie Counter", user_profile.get_cookie_clicks, "Distance:", circle_distance)
                    if event.type == pygame.QUIT:
                        print("end game")
                        running = False

                    #key presses
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        save_data(user_profile)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        print("Stats")
                        print(f"Current Cookies: {user_profile.get_cookie_clicks}")
                        print(f"Current Level: {user_profile.level}")

                #draw images, pygame stuff
                pygame.draw.circle(screen, "white", (screen_size[0]/2, screen_size[1]/2), 250)
                screen.blit(cookie_image, cookie_image.get_rect(center=window.center))
                cookie_text = font.render(f"Cookies Clicked: {user_profile.get_cookie_clicks}", True, "black")
                level_text = font.render(f"Current Level: {user_profile.level}", True, "black")
                screen.blit(cookie_text, (screen_size[0]/2, screen_size[1]/8))
                screen.blit(level_text, (screen_size[0]/3, screen_size[1]/8))
                pygame.display.flip()
                clock.tick(60)
        finally:
            save_data(user_profile)
            pygame.quit()


if __name__ == "__main__":
    main()

import pygame 
import sys, os
import time, csv

pygame.init()

# file path
local_time = time.localtime()
time_str = time.strftime("%Y%m%d%H%M%S", local_time)
print(time_str)
default_dir = os.getcwd() + '/saved_data/'
default_file = 'record_trace_' + time_str + '.csv'

# argument
if len(sys.argv) > 2:
    print("Too many argument!")
    exit()
elif len(sys.argv) == 2:
    file_name = default_dir + sys.argv[1]
    print("Recorded file will be saved as \"%s\"" % sys.argv[1])
else:
    file_name = default_dir + default_file
    print("The file will be saved as \"%s\""% default_file)




# first frame
screen = [800, 600]
screen_center = (screen[0]/2, screen[1]/2) # make screen_center as tuple
window_surface = pygame.display.set_mode(screen)
pygame.display.set_caption('Mouse Trace :)')
window_surface.fill((255, 255, 255)) # white background
pygame.display.update()

# define text
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font('freesansbold.ttf', 32)
text_to_start = font.render('Move Mouse to Start', True, blue)
text_rect = text_to_start.get_rect(center=(screen_center))
text_rect2 = text_to_start.get_rect(center=(screen[0]/2, screen[1]/2 + 40))
text_recording = font.render('Now Recording', True, blue)
text_prepare_to_quit = font.render('Press Q to Quit', True, blue)
text_quit = font.render('Press Esc to Quit', True, blue)

xposCenter = screen_center[0]
yposCenter = screen_center[1]
print("center is", xposCenter, yposCenter)
pygame.mouse.set_pos(screen_center)
[xpos, ypos] = pygame.mouse.get_pos()

# force default mouse position 
window_surface.fill((255, 255, 255))
window_surface.blit(text_to_start, text_rect)
pygame.display.update()
while pygame.mouse.get_pos() != screen_center:
    pygame.mouse.set_pos(screen_center)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
# update after mouse centered
window_surface.fill((255, 255, 255))
window_surface.blit(text_recording, text_rect)
window_surface.blit(text_prepare_to_quit, text_rect2)
pygame.display.update()

# Now recording
prepare_to_quit = 0
this_list = [time.time(), xpos, ypos, 0.0]
last_list = [time.time(), xpos, ypos, 0.0]
with open(file_name, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['POSIXtime', 'x_pos', 'y_pos', 'pixel'])
    while True:
        [xpos, ypos] = pygame.mouse.get_pos()
        if (xpos, ypos) != screen_center:
            distance = (float(xpos - xposCenter)**2 + float(ypos -yposCenter)**2)**0.5
            this_list = [time.time(), xpos, ypos, distance]
            print(this_list)
            if (last_list[1], last_list[2]) == screen_center:
                writer.writerow(last_list)
            writer.writerow(this_list)
            last_list = this_list # update old
        else:
            # or update zero distance
            last_list = [time.time(), xpos, ypos, 0.0]

        pygame.mouse.set_pos(screen_center)
        time.sleep(0.001)

        # detect quit condition
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    prepare_to_quit = 1
                    window_surface.fill((255, 255, 255))
                    window_surface.blit(text_recording, text_rect)
                    window_surface.blit(text_quit, text_rect2)
                    pygame.display.update()
                if event.key == pygame.K_ESCAPE:
                    if prepare_to_quit:
                        pygame.quit()
                        sys.exit()


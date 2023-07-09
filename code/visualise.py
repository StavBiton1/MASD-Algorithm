# Partially copied from https://www.youtube.com/watch?v=JtiK0DOeI4A

import pygame
import datetime
import csv

# filename = input("The name of a file with pathfinding log: ")
csv_file = "../code/small_map.csv"
WINDOW_WIDTH = 575  # Adjust the window width to your preference
WINDOW_HEIGHT = 640  # Adjust the window height to your preference
WIDTH = 640
PRINT_ID = True
RAD = 0.3
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MAPF Visualisation")

agent_colors = [
    (64, 224, 208),
    (255, 165, 0),
    (128, 0, 128),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0),
    (255, 128, 128),
    (25, 128, 128),
    (25, 0, 50),
    (100, 0, 50),
    (200, 50, 50),
    (128, 128, 0)
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)


class Map:
    def create_map_image_from_csv(csv_file):
        map_image = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                row_values = []
                for value in row:
                    if value == '0':
                        row_values.append('.')
                    elif value == '1':
                        row_values.append('@')
                    else:
                        # Handle other cases if needed
                        row_values.append('.')
                map_image.append(row_values)
        return map_image

    def __init__(self, map_image, rows,cols):
        self.rows_ = rows
        self.cols_ = cols
        self.obstacles_ = []
        for i in range(rows):
            for j in range(cols):
                if map_image[i][j] == '@':
                    self.obstacles_.append((j, i))

    def draw_obstacles(self, win, width):
        gap = width // self.rows_

        for cell in self.obstacles_:
            i = cell[0]
            j = cell[1]
            pygame.draw.rect(win, BLACK, (i * gap, j * gap, gap, gap))

    def draw_lines(self, win, width):
        gap = width // self.rows_

        for i in range(self.rows_+1):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(self.cols_):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    def draw(self, win, width):
        win.fill(WHITE)
        self.draw_lines(win, width)
        self.draw_obstacles(win, width)


class Agent:
    def __init__(self, agent_path_line, cell_width):
        self.path_ = []
        self.path_index_ = 0
        self.time_ = 0
        self.gap_ = cell_width
        
        parsed_locations = []
        #for x in range(len(agent_path_line)):
         #   parsed_locations.append(list(map(int, agent_path_line[x][8:].split())))
        #parsed_locations = [int(x) for x in agent_path_line[x][1:]]  # Exclude the agent identifier
        parse = agent_path_line.split()
        # parse[0] == "Agent"
        # parse[1] == agent_ID
        parsed_locations = list(map(int, parse[2:]))
        #for j in range(len(parsed_locations)):
         #   self.ID_ = int(j+1)
        #for i in range(0, len(parsed_locations[j]), 3):
         #       self.path_.append(
          #          (parsed_locations[j][i + 1] * cell_width,
           #         parsed_locations[j][i] * cell_width,
            #        parsed_locations[j][i + 2]))
        for i in range(0, len(parsed_locations), 3):
            self.path_.append(
                (parsed_locations[i] * cell_width,
                 parsed_locations[i+1] * cell_width, 
                 parsed_locations[i + 2]))

        self.ID_ = int(parse[1])
            
        '''
        for i in range(0, len(agent_data), 2):
            time_step = agent_data[i]
            location = agent_data[i + 1]
            if isinstance(location, datetime.datetime):
                location = location.timestamp()
            self.path_.append((location[1] * cell_width, location[0] * cell_width, time_step))
        '''
        
        self.color_ = agent_colors[self.ID_ % len(agent_colors)]



        assert len(self.path_) >= 2
        self.x_ = self.path_[0][0]
        self.y_ = self.path_[0][1]

        self.visible_ = True if self.path_[0][2] == 0 else False

    def move(self, delta_time, time_direction):
        assert time_direction == 1 or time_direction == -1

        self.time_ += delta_time * time_direction* 60 / 5  # Convert delta_time to time steps
        if self.time_ < 0:
            self.time_ = 0
        if self.time_ < self.path_[0][2]:
            self.visible_ = False
            return

        self.visible_ = True

        if time_direction == 1:
            while self.path_index_ + 2 < len(self.path_) and self.path_[self.path_index_ + 1][2] < self.time_:
                self.path_index_ += 1
        else:
            while self.path_index_ >= 1 and self.path_[self.path_index_][2] > self.time_:
                self.path_index_ -= 1

        next_cell = self.path_[self.path_index_ + 1]
        cur_cell = self.path_[self.path_index_]

        plan_delta = next_cell[2] - cur_cell[2]
        real_delta = self.time_ - cur_cell[2]
        if real_delta > plan_delta:
            real_delta = plan_delta
        if plan_delta == 0:
            alpha =0
        else:
            alpha = real_delta / plan_delta

        delta_x = next_cell[0] - cur_cell[0]
        delta_y = next_cell[1] - cur_cell[1]

        self.x_ = cur_cell[0] + alpha * delta_x
        self.y_ = cur_cell[1] + alpha * delta_y

    def draw(self, win):
        if not self.visible_:
            return

        pygame.draw.circle(win, self.color_, (self.x_ + self.gap_ // 2, self.y_ + self.gap_ // 2), RAD * self.gap_)

        if PRINT_ID:
            font = pygame.font.SysFont("Tahoma", 12)
            text = font.render(str(self.ID_), False, (10, 180, 10))
            win.blit(text, (self.x_, self.y_))

class Animation:
    def main(win, width, csv_file, agent_data):
        global RAD, PRINT_ID

        data = []
        speed_mode = 0.5

        map_image = Map.create_map_image_from_csv(csv_file)
        rows = len(map_image)  # Number of rows in the map
        columns = len(map_image[0])  # Number of columns in the map

        agents = [Agent(agent_data[0][i], width // max(rows, columns)) for i in range(len(agent_data[0]))]
        #for i in range(len(agent_data[0])):
         #   agents = [Agent(agent_data[0][i]), width // max(rows, columns)]
        agents[0].path_=[(0, -58, 0), (0, -58, 1), (0, -58, 2), (0, -58, 3),(0,0,4),(0,58,5),(58,58,6),(58,58,7),(116,58,8),(174,58,9),(232,58,10),(290,58,11),(348,58,12),(406,58,13),(464,58,14),(464,0,15),(406,0,16),(348,0,17),(290,0,18),(232,0,19),(174,0,20),(116,0,21),(58,0,22),(0,0,23),(0,-58,24) ]
        agents[1].path_=[(58, -58, 0), (58, 0, 1), (58, 58, 2),(0, 58, 3),(0, 116, 4), (0, 174, 5),(0,232,6),(0,290,7),(58,290,8),(116,290,9),(116,290,10),(174,290,11),(232,290,12),(290,290,13),(348,290,14),(406,290,15),(464,290,16),(464,232,17),(464,174,18),(464,116,19),(464,58,20),(464,0,21),(406,0,22),(348,0,23),(290,0,24),(232,0,25),(174,0,26),(116,0,27),(58,0,28),(58,-58,29)]
        agents[2].path_=[(116, -58, 0), (116, -58, 1), (116, -58, 2),(116, -58, 3),(116, -58, 4),(116, -58, 5),(116, -58, 6),(116, 0, 7),(116,0,8),(116,58,9),(116,58,10),(174,58,11),(232,58,12),(290,58,13),(348,58,14),(406,58,15),(464,58,16),(464,0,17),(406,0,18),(348,0,19),(290,0,20),(232,0,21),(174,0,22),(116,0,23),(116,-58,24)]
        agents[3].path_=[(174, -58, 0), (174, 0, 1), (232, 0, 2), (290, 0, 3),(348,0,4),(348,58,5),(406,58,6),(406,116,7),(406,174,8),(406,232,9),(406,290,10),(406,348,11),(406,406,12),(406,464,13), (406,522,14), (348,522,15),(348,522,16),(348,522,17),(406,522,18),(406,464,19),(406,406,20), (406,348,21), (406,290,22),(406,232,23),(406,174,24),(406,116,25),(406,58,26),(348,58,27),(290,58,28),(232,58,29),(174,58,30),(174,0,31), (174,-58,32) ]
        environment = Map(map_image, rows, columns)

        run = True
        time = 0
        delta = 1
        animate = True

        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont("Tahoma", 24)
        last_time = pygame.time.get_ticks()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        animate = not animate

                    if event.key == pygame.K_r:
                        animate = True
                        delta = -delta

                    if event.key == pygame.K_UP:
                        speed_mode += 1

                    if event.key == pygame.K_DOWN and speed_mode > 1:
                        speed_mode -= 1

                    if event.key == pygame.K_i:
                        PRINT_ID = not PRINT_ID

            environment.draw(win, width)
            #text = font.render("Map", False, (10, 180, 10))
            #win.blit(text, (20, 20))


            now_time = pygame.time.get_ticks()
            delta_time = (now_time - last_time) / 1000.0
            last_time = now_time

            for agent in agents:
                if animate:
                    agent.move(delta_time * speed_mode, delta)
                agent.draw(win)

            if animate:
                time += delta_time * speed_mode * delta
            if time < 0:
                time = 0
            #text = font.render("Time is " + str(int(time)), False, (10, 180, 10))
            #win.blit(text, (20, 20))
                            
            pygame.display.update()

        pygame.quit()

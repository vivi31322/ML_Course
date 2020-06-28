class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            coingrid=set()
            speed_ahead = 1000
            leah=1200
            #leaf=0
            riah=1200
            #riaf=0
            if self.car_pos[0] <= 65: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 565: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for coin in scene_info["coins"]:
                x = coin[0]- car["pos"][0] # x relative position
                print(coin)
                y = coin[1]- car["pos"][1] # y relative position
                if x <= 40 and x >= -40 :      
                    if y > 0 and y < 300:
                        coingrid.add(2)
                        if y < 200:
                            coingrid.add(5) 
                    elif y < 0 and y > -200:
                        coingrid.add(8)
                if x > -100 and x < -40 :
                    if y > 80 and y < 250:
                        coingrid.add(3)
                    elif y < -80 and y > -200:
                        coingrid.add(9)
                    elif y < 80 and y > -80:
                        coingrid.add(6)
                if x < 100 and x > 40:
                    if y > 80 and y < 250:
                        coingrid.add(1)
                    elif y < -80 and y > -200:
                        coingrid.add(7)
                    elif y < 80 and y > -80:
                        coingrid.add(4)
            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                            riah=car["velocity"]
                        elif y < -80 and y > -200:
                            grid.add(9)
                            #riaf=car["velocity"]
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                            leah=car["velocity"]
                        elif y < -80 and y > -200:
                            grid.add(7)
                            #leaf=car["velocity"]
                        elif y < 80 and y > -80:
                            grid.add(4)
            return move(coingrid=coingrid,grid= grid, speed_ahead = speed_ahead, leah=leah ,riah=riah )
            
        def move(coingrid,grid, speed_ahead,leah ,riah ): 
            # if self.player_no == 0:
            #     print(grid)
            if len(grid) == 0:
                if (1 in coingrid) or (4  in coingrid):
                    return ["SPEED","MOVE_LEFT"]
                elif (3 in coingrid) or (6  in coingrid):
                    return ["SPEED","MOVE_RIGHT"]
                else:
                    return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if (1 in coingrid) or (4  in coingrid):
                        return ["SPEED","MOVE_LEFT"]
                    elif (3 in coingrid) or (6  in coingrid):
                        return ["SPEED","MOVE_RIGHT"]
                    else:
                        return ["SPEED"]
                else:
                    if(self.car_pos[1]>=730):
                        return ["SPEED"]
                    if (5 in grid): # NEED to BRAKE
                        if (4 not in grid) :
                            if(1 not in grid) or (self.car_vel < leah): # turn left 
                                return ["SPEED", "MOVE_LEFT"]
                            elif self.car_vel == leah:
                                return ["MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) :
                            if(3 not in grid) or (self.car_vel < riah): # turn left 
                                return ["SPEED", "MOVE_RIGHT"]
                            elif self.car_vel == riah:
                                return ["MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel <= speed_ahead:  # BRAKE
                                #return ["SPEED"]
                                if (1 in coingrid) or (4  in coingrid):
                                    return ["SPEED","MOVE_LEFT"]
                                elif (3 in coingrid) or (6  in coingrid):
                                    return ["SPEED","MOVE_RIGHT"]
                                else:
                                    return ["SPEED"]
                            else:
                                if (7 in coingrid) or (4  in coingrid):
                                    return ["BRAKE","MOVE_LEFT"]
                                elif (9 in coingrid) or (6  in coingrid):
                                    return ["BRAKE","MOVE_RIGHT"]
                                else:
                                    return ["BRAKE"]
                    if (self.car_pos[0] < 60 ):
                        return ["SPEED", "MOVE_RIGHT"]
                    if (self.car_pos[0] > 740 ):
                        return ["SPEED", "MOVE_LEFT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid):
                        if self.car_vel<leah: # turn left 
                            return ["SPEED","MOVE_LEFT"]   
                        elif self.car_vel>leah:
                            return["BRAKE","MOVE_LEFT"] 
                        else:
                            return["MOVE_LEFT"] 
                    if (6 not in grid) and (9 not in grid): # turn right
                        if self.car_vel<riah: # turn left 
                            return ["SPEED","MOVE_RIGHT"]   
                        elif self.car_vel>riah:
                            return["BRAKE","MOVE_RIGHT"] 
                        else:
                            return["MOVE_RIGHT"] 
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass

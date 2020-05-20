"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import random
def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    block_pre=0
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            #if scene_info["platform_1P"][0]+20 ==(pred) : return 10*random.random()%2+1  # NONE
            if scene_info["platform_1P"][0]+20  > (pred-3) and scene_info["platform_1P"][0]+20 < (pred+3): return 10*random.random()%2+1#0  # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-3) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
    def pred_X(base,ball_x,ball_y,speed_x,speed_y):
        x =abs( ( base-ball_y) // speed_y) # 幾個frame以後會需要接  # x means how many frames before catch the ball
        pred = ball_x+(speed_x*x)  # 預測最終位置 # pred means predict ball landing site 
        bound = pred // 200 # Determine if it is beyond the boundary
        if (bound > 0): # pred > 200 # fix landing position
            if (bound%2 == 0):
                pred = pred - bound*(197+10*random.random()%4) 
            else :
                pred = 200 - (pred - 197*bound)
        elif (bound < 0) : # pred < 0
            if (bound%2 ==1) :
                pred = abs(pred - (bound+1) *200)
            else :
                pred = pred + (abs(bound)*(197+10*random.random()%4))
        return pred

    def ml_loop_for_1P(block_sp): 
        block_x=scene_info["blocker"][0]
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            predi=pred_X(scene_info["platform_1P"][1],scene_info["ball"][0],scene_info["ball"][1],scene_info["ball_speed"][0],scene_info["ball_speed"][1])
            if 230<scene_info["ball"][1] and 290>scene_info["ball"][1]:
                x = ( 270-scene_info["ball"][1]) // scene_info["ball_speed"][1]
                bx=scene_info["blocker"][0]+x*block_sp
                x=scene_info["ball"][0]+x*scene_info["ball_speed"][0]
                if x<bx+40 and x>=bx-10:
                    predi=pred_X(scene_info["platform_1P"][1],x,270,-scene_info["ball_speed"][0],scene_info["ball_speed"][1]) 
            return move_to(player = '1P',pred = predi)
        else :# 球正在向上 # ball goes up
            if scene_info["ball"][1]>280:
                predi=100
                x = pred_X(scene_info["ball"][1],scene_info["ball"][0],270,scene_info["ball_speed"][0],scene_info["ball_speed"][1])#(scene_info["ball"][1]-270) // scene_info["ball_speed"][1]
                bx=scene_info["blocker"][0]+x*block_sp
                #x=scene_info["ball"][0]+x*scene_info["ball_speed"][0]
                if x<bx+40 and x>=bx-10:
                    predi=pred_X(scene_info["platform_1P"][1],x,270,scene_info["ball_speed"][0],-scene_info["ball_speed"][1])
                return move_to(player='1P',pred=predi)
            else:
                return move_to(player = '1P',pred = 100)
        



    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
            block_pre=0
            
        else:
            if side == "1P":
                b=scene_info["blocker"][0]-block_pre
                command = ml_loop_for_1P(b)
                block_pre=scene_info["blocker"][0]
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})

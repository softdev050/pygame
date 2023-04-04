
def create_enemy(type, damage, hp):
    print(f"Enemy: {type, damage, hp, difficulty}")
    
difficulty = "medium"

difficulty_damage = {
    "easy" : {
        "enemy1" : [20, 5],
        "enemy2" : [12, 8],
    },
    
    "medium" : {
        "enemy1" : [25, 8],
        "enemy2" : [15, 10],
    },
    
    "hard" : {
        "enemy1" : [30, 10],
        "enemy2" : [20, 12],
    },
}

create_enemy("enemy1", difficulty_damage[difficulty]["enemy1"][0],difficulty_damage[difficulty]["enemy1"][1])
create_enemy("enemy2", difficulty_damage[difficulty]["enemy2"][0],difficulty_damage[difficulty]["enemy2"][1])
create_enemy("enemy2", difficulty_damage[difficulty]["enemy2"][0],difficulty_damage[difficulty]["enemy2"][1])


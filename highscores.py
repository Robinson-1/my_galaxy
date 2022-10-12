import os
from datetime import date

def check_highscore(self):
    # checks for highscore, if none return None.
    if not os.path.exists(self.SCORE_FILENAME):
        return None
    with open(self.SCORE_FILENAME, "r") as file:
        top_score = int(file.readline().split(",")[2])
    print(str(top_score))
    return top_score

def update_highscores(self):
    #Function to update highscores files
    date_today = date.today().strftime("%d/%m/%Y")
    if not self.check_highscore():
        with open(self.SCORE_FILENAME, "w") as file:
            file.write(f"{self.player_name},{date_today},{self.current_y_loop}\n")
        return
    with open(self.SCORE_FILENAME, "r") as file:
        lines = file.readlines()
        high_scores = [line.split(",") for line in lines]

    high_scores.append([self.player_name,date_today,str(self.current_y_loop) + "\n"])
    high_scores.sort(key=lambda row: int(row[2]))

    with open(self.SCORE_FILENAME, "w") as file:
        for i, score in enumerate(high_scores[::-1]):
            file.write(",".join(score))
            if i == 20:
                break
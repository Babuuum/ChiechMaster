from enum import Enum

class LeagueFormat(Enum):
    CHILL = 'chill'  # duration 2 weeks
    SOFT = 'soft'    # duration 1 month
    NORMAL = 'normal' # duration 3 month

class GoalsDifficult(Enum):
    VERY_EASY = 'very_easy'
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'
    INSANE = 'insane'

class MedsDayTime(Enum):
    BEFORE_BREAKFAST = 'BEFORE_BREAKFAST'
    BREAKFAST = 'BREAKFAST'
    AFTER_BREAKFAST = 'AFTER_BREAKFAST'
    BEFORE_LUNCH = 'BEFORE_LUNCH'
    LUNCH = 'LUNCH'
    AFTER_LUNCH = 'AFTER_LUNCH'
    DINNER = "DINNER"
    BEFORE_DINNER = "BEFORE_DINNER"
    AFTER_DINNER = "AFTER_DINNER"
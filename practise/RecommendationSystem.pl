% EasyWash Cycle Recommendation System

% Rule 1:
recommendation(1, 1, 1, 1):- cycle(1).

% Rule 2:
recommendation(2, 1, 2, 1):- cycle(2).

% Rule 3:
recommendation(1, 2, 2, _):- cycle(3).

% Rule 4:
recommendation(2, 2, 2, 2):- cycle(4).

% Define Facts (Cycles):
cycle(1).
cycle(2).
cycle(3).
cycle(4).
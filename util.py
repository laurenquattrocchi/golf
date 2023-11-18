def h_adjusted_score(holes:list, scores:list, p_handicapp:int, num_played=18)->list:
    '''
    adjusts scores for handicapp, lower handicapp of hole, hard the hole is
    ex: if handicapp 14 get stroke on hardest 14 holes, if handicapp > 18, 
    take 1 stroke from all 18 and 2 from remaining (handicapp-18) holes, 
    if > 36, 2 from each hole and 3 from (handicapp-36) holes etc..
    if handicapp of hole is <= to your handicapp you get a stroke on that hole
    input: 
        holes: list of handicapps per hole, index+1 correspondes to hole number
        scores: list of scores for round, index+1 corresponds to hole number
        p_handicapp: int, handicapp of player 
        num_played: int, default 18, pass 9 if only play 9 holes
    output:
        scores: list of adjusted scores
    '''

    # if only play 9 holes
    if num_played==9:
        holes = holes[:9]
        scores = scores[:9]

    # convert from string to int
    scores = [int(score) for score in scores]

    if p_handicapp > 18:
        strokes = int(p_handicapp/18)
        if strokes > 0:
            scores = [x - strokes for x in scores]

    for i,hole in enumerate(holes):
        _,h_handicapp = hole
        if h_handicapp <= p_handicapp:
            scores[i] = scores[i]-1

    return scores

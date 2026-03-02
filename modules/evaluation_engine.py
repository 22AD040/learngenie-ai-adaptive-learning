def evaluate_answers(user_answers, correct_answers):
    score = 0
    
    for q in correct_answers:
        if q in user_answers:
            if user_answers[q] == correct_answers[q]:
                score += 20

    return score
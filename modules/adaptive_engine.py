def update_level(score):
    if score >= 80:
        return "Advanced"
    elif score >= 50:
        return "Intermediate"
    else:
        return "Beginner"
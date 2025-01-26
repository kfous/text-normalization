

def calculate_performance(s, e):
    performance_seconds = e - s
    # Convert seconds to hours and minutes
    hours = int(performance_seconds // 3600)
    minutes = int((performance_seconds % 3600) // 60)
    seconds = int(performance_seconds % 60)
    # Format and Print the script's performance in hours, minutes, and seconds
    performance_message = (
        "Performance: {:02d} hours {:02d} minutes {:02d} seconds".format(
            hours, minutes, seconds
        )
    )
    print("{}".format(performance_message))
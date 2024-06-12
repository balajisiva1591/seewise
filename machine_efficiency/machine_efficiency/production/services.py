from datetime import timedelta

def calculate_oee(production_logs):
    available_time = 3 * 8  # total available time in hours for 3 shifts
    ideal_cycle_time = 5 / 60  # 5 minutes in hours

    total_duration = sum(log.duration for log in production_logs)
    if total_duration == 0:  # Check if total duration is zero
        return {
            'availability': 0,
            'performance': 0,
            'quality': 0,
            'oee': 0
        }

    actual_output = len(production_logs)
    good_products = sum(1 for log in production_logs if abs((log.end_time - log.start_time).total_seconds() / 60 - 5) < 1)
    
    availability = (available_time - (available_time - total_duration)) / available_time * 100
    performance = (ideal_cycle_time * actual_output) / total_duration * 100
    quality = good_products / actual_output * 100

    oee = availability * performance * quality / 10000
    return {
        'availability': availability,
        'performance': performance,
        'quality': quality,
        'oee': oee
    }

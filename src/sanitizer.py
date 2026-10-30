"""
Sensor Data Sanitizer
Module for cleaning and normalizing raw sensor readings.
"""

def clean_sensor_readings(readings):
    """
    Cleans and normalizes a list of sensor values.

    Rules applied:
    1. Drop None, non-numeric values (or unparseable strings), and negative error flags (< 0).
    2. Convert valid elements to float.
    3. Cap/clip values exceeding 500.0 to 500.0.
    4. Handle empty lists or lists with no valid entries gracefully by returning [].

    Args:
        readings (list): List containing mixed data types (numbers, strings, None, etc.)

    Returns:
        list[float]: Cleaned, filtered, and clipped float values.
    """
    if not readings or not isinstance(readings, (list, tuple)):
        return []

    cleaned_data = []

    for item in readings:
        # Skip None or empty string values directly
        if item is None:
            continue

        try:
            val = float(item)
        except (ValueError, TypeError):
            # Skip items that cannot be parsed into numbers (e.g., 'ERR', 'N/A', objects)
            continue

        # Drop negative readings (used as hardware error flags)
        if val < 0.0:
            continue

        # Clip values greater than upper threshold
        if val > 500.0:
            val = 500.0

        cleaned_data.append(val)

    return cleaned_data

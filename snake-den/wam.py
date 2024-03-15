def calculate_wam(units, marks):
    """
    Calculates the Weighted Average Mark (WAM) based on the given units and marks.
    
    Args:
        units (list): A list of unit values (e.g., credit points) for each subject.
        marks (list): A list of marks obtained for each subject.
        
    Returns:
        float: The calculated WAM.
    """
    total_units = sum(units)
    weighted_marks = [units[i] * marks[i] for i in range(len(units))]
    total_weighted_marks = sum(weighted_marks)
    
    wam = total_weighted_marks / total_units
    
    return wam

# Example usage
units = [6, 3, 4, 2]
marks = [75, 82, 69, 88]

student_wam = calculate_wam(units, marks)
print(f"The student's WAM is: {student_wam:.2f}")

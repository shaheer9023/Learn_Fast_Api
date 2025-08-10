def grades(marks):
    sum=0
    for mark in marks.values():
        sum+=mark
    final_marks=round((sum/len(marks)),2)
    print(final_marks)

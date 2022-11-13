'''
Pseudo Code for algorithm implementation

class Grouper():

    students: list[models.SurveyRecord]
    groups: list[models.GroupRecord]
    def group_students(students):
      sorted_student_list = sort_students(students)
      
      while len(sorted_student_list) > 0:
          # add_user_to_group:
          student = sorted_student_list.pop()
        
        
    def add_student_to_group(student):
        for group in self.groups:
            if not len(group) < criteria:
                continue
            
            if student_meets_group_criteria:
                group.add_student(student)
                return
        
        # groups were full or they didn't meet the criteria. Now we need to start the swapping logic
        
        for group in self.groups:
            if student_meets_group_criteria:
                find_the_person_to_swap()
                swap_user(student)
                return
        
        # no criteria were met
        add_student_to_leftover_pile_for_later():
        
        

  
  
  
def sort_students(students):
  for each student in students
    look at the criteria.
    
    For dislikes:
      
    For availability:  
      look at how often they are available. Count the total number of slots they are available. 
      Rank the availability compared to when others fit the available slots

    For preferred students:
      if there are preferred students, it means they may have a more refined interest, 
      For ties, the least preferred count means higher compatibility
      
def student_score():
  dislikes = total_dislikes_for_the_user(student)
  likes = len(students)-dislikes   
      
def total_dislikes_for_the_user(student):
      look at the number of times their name shows up in dislikes 
      and also append the number of people they dislike. 
      This should be the total count of incompatible people for the student. 
      If the dislike is reciprical, don't count it twice.
    
    first add each of the student's non preferred students to the set.
    disliked_set = {}
    
    for student in students:
        if student.non_preferred_students.contains(this_student):
            disliked_set.add(student.student_id)
            
    return len(disliked_set)
      
def get_total_preferred_slots():
  first 
  
def build_map_of_availability_across_dataset():
  dict[day_of_week, dict[time_of_day, availability_count]  
  avail_map = {}
  for student in students:
    for day in week:
      avail_map

'''


def total_dislike_incompatible_students(student, students):
    """
    function to identify the total number of students that are disliked 
    ook at the number of times their name shows up in dislikes
    and also append the number of people they dislike.
    This should be the total count of incompatible people for the student.
    If the dislike is reciprical, don't count it twice.
    """
    # first add each of the student's non preferred students to the set.
    disliked_set = {}

    for student in students:
        if student.non_preferred_students.contains(this_student):
            disliked_set.add(student.student_id)

    return len(disliked_set)

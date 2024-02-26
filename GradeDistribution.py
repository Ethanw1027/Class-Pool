import pandas as pd
import ratemyprofessor

school = ratemyprofessor.get_school_by_name("Virginia Tech")
grades_data_file = "databases/grades.csv"

class GradeDistribution:
    def __init__(self, grades_data_file):
        self.df = pd.read_csv(grades_data_file)
    
    def list_depts(self):
        dept_list = self.df["Subject"].unique()
        return list(dept_list)
    
    def search_class(self, course_dept, course_num):
        course_data = self.df
        course_dept = str(course_dept).upper()
        course_data = course_data[course_data["Subject"] == course_dept]
        course_data = course_data[course_data["Course No."] == int(course_num)]
        return course_data
    
    def get_prof_gpas(self, course_data):
        avg_gpa_by_instructor = course_data.groupby('Instructor')['GPA'].mean()
        ranked_profs = avg_gpa_by_instructor.sort_values(ascending=False)
        return ranked_profs
    
    def get_prof_rating(self, prof_name):
        prof = ratemyprofessor.get_professor_by_school_and_name(school, prof_name)
        return prof.rating

#    def rank_profs(self, course_dept, course_num):
#        course_data = self.search_class(course_dept, course_num)
#        prof_data = self.get_prof_gpas(course_data)
#        
#        prof_ratings = []
#        for prof_name, gpa in prof_data.items():
#            rating = self.get_prof_rating(prof_name)
#            prof_ratings.append({"Name": prof_name, "GPA": gpa, "Rating": rating})
#        
#        ranked_df = pd.DataFrame(prof_ratings)
#        return ranked_df


grade_dist = GradeDistribution(grades_data_file)
#print(grade_dist.rank_profs("CS", "2114"))

#grade_dist.get_prof_rating("Esakia")
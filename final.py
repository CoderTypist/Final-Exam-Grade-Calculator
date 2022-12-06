import numpy as np
from typing import List, Tuple


class Category:
    
    def __init__(self, name: str, percentage: float, grades: List[Tuple[float, float]]):
        self.name = name
        self.percentage = percentage
        self.grades = grades
        
    def grade(self) -> float:
        scaled = [ (points*100)/maximum for points, maximum in self.grades ]
        return np.mean(scaled)
    
    def __repr__(self) -> str:
        return f'{self.name:>15}:  {self.percentage:>6.2f}%:  {self.grade():6.2f}'
        

class Course:
    
    def __init__(self, name: str):
        self.name = name
        self.categories = []
        
    def add_category(self, category: Category):
        self.categories.append(category)
        
    def total_points(self) -> float:
        return np.sum([ cat.percentage for cat in self.categories ])
    
    def incorporate_final(self, course_grade_wanted: float) -> float:
        exam_percentage = 100 - self.total_points()
        scaled_grade = self.grade()*(self.total_points()/100)
        points_needed = course_grade_wanted - scaled_grade
        exam_grade = 0 if points_needed <= 0 else (points_needed*100)/exam_percentage
        self.add_category(Category('Final', exam_percentage, [(exam_grade,100)]))
    
    def category_contributions(self) -> Tuple[float, float]:
        total_points = self.total_points()
        points_earned = [ cat.grade()*(cat.percentage/total_points) for cat in self.categories ]
        points_possible = [ (cat.percentage*100)/total_points for cat in self.categories ]
        return zip(points_earned, points_possible)
    
    def grade(self) -> float:
        return np.sum([ contribution[0] for contribution in self.category_contributions() ])
    
    def __repr__(self) -> str:
        s = f'{self.name}:\n\n'
        s += f'          Grade:   {self.grade():.2f}%\n\n'
        for category, contribution in zip(self.categories, self.category_contributions()):
            s += f'{category} -> ( {contribution[0]:5.2f} / {contribution[1]:5.2f} )\n'
        return s
    

def main():
    
    course = Course('Computer Science Course')
    
    course.add_category(Category('Homework', 30, 
                                 [(90,100),(90,100),(90,100),(90,100),(90,100)]))
    
    course.add_category(Category('Midterms', 25,
                                 [(55,60),(55,60)]))
    
    course.add_category(Category('Project', 20,
                                 [(90,100)]))
    
    course.incorporate_final(90)
    
    print(course)
    

if __name__ == '__main__':
    main()

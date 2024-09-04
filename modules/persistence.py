from typing import List
from dataclasses import dataclass, field

@dataclass
class QuizQuestion:
   question: str
   correctAnswer: str
   wrongAnswers: List[str]
   timeout: int = field(default=15)
   
   def __repr__(self):
      return self.question
     

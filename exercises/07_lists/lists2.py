# lists2.py

# Below we have defined two lists: quiz_questions and quiz_answers.
# You should write a function get_question_and_answer that takes a list of questions,
# a list of answers and an index and return a tuple (similar to a list, you will learn more later),
# with the specific question and answer at that index.
# For this you will need to know how to access a list item at a specific index.

### I AM NOT DONE


quiz_questions = [
  "How tall is Mount Everest (in meters)?",
  "How old is the oldest tree on earth (in years)?",
  "How long does it take the earth to circle the sun (in days)?"
]

quiz_answers = [8849, 4853, 365]


def get_question_and_answer(questions: list, answers: list, index: int) -> tuple:
    return (questions, answers)


# Don't modify code below, 
# but you can take a look and try to understand it
# this time we're using a while loop

index = 0

while index < len(quiz_questions):
    (question, answer) = get_question_and_answer(quiz_questions, quiz_answers, index)

    if not isinstance(question, str):
        raise ValueError("question should be a string")
    if not isinstance(answer, int):
        raise ValueError("answer should be an integer")
    
    print(question)
    print(answer)
    index+=1
# How to use pylet as a teacher in a course

1. How does pylet work
2. Adjusting/changing/replacing exercises:
   - Exercise folder
   - Exercise yaml
3. Getting student progress

## 1. How does pylet work?

Pylet is a tool to learn python by solving python exercises. The ultimate learning by doing.
For this you give students unfinished python exercises, that either don’t run successfully and have to be fixed or that you have written tests for at the bottom of the file that won’t pass until the student solves the exercise.

When you use pylet on your own, there a list of exercises written for you to teach you the basics of python. Aside from exercises you have a README for each section, which gives you a small introduction to the topic of the section and additional sources for you to look up if you are stuck.

When you are using pylet as part of a course, you might want to adjust the exercises. Maybe you want to remove exercises, change them, add more or change the order. Maybe you want to write completely new exercises, that fit your course material better.

In this document, you can learn how to adjust the pylet exercises to your course.

## 2. Adjusting exercises

To write an exercise in pylet you need to do two things.

### 1. Create exercise file

Create a python file (your exercise file) in the exercises folder and add the exercise code, including the # I AM NOT DONE comment that gives students the opportunity to play around with an exercise after they have already gotten it to run.

### 2. Add exercise info to exercise_info.yaml

Add the exercise to the exercise_info.yaml file. Here each exercise has the following format:

```yaml
<exercise_name>:
  path: <exercise_path>
  test: <test_boolean>
```

The order of the exercises in the exercise_info.yaml file determines the order that pylet will ask students to solve the exercises in.

## 3. Getting student progress

When using pylet as part of a course, you will likely want to be informed about your students progress. One tool that you will have access to is using git and GitHub.
Your students can clone the pylet repository (or rather, your version of the repository with the correct exercises) and commit and push their progress to their own repository. That way you can look at their progress and introduce them to working with git and GitHub early as well.

Now this has some disadvantages. It might not be the best way to go, to have every student's repository locally on your machine to keep up to date with their progress.
It also might not be in your interest to introduce students to git & GitHub early as it might confuse beginners that are just learning to program.

For this you and your students have another tool: `python pylet summary.`
With this pylet command the students can generate a summary.zip, which they can share with you. It includes a folder with the completed exercises, the current exercise file that the student is solving and a summary markdown file, which includes an overview of what is included and completed.

This way you can have students share their progress easily, check out their completed exercises and help them with the current exercise, if they are stuck.

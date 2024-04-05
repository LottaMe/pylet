# from exercise import Exercise
# from interface import Interface


# class TestExercise:
#     path = "tests/mocks/mock_exercise.py"
#     interface = Interface()

#     def test_compile(self):
#         exercise = Exercise(path=self.path, interface=self.interface)

#         f = open(self.path, "w")
#         f.write("print 'hello world'")
#         f.close()

#         result_fail = exercise.compile()
#         assert result_fail.success == False
#         assert len(result_fail.output) > 0 and isinstance(result_fail.output, str)

#         f = open(self.path, "w")
#         f.write("print('hello world')")
#         f.close()

#         result_success = exercise.compile()
#         assert result_success.success == True
#         assert len(result_fail.output) > 0 and isinstance(result_success.output, str)

#         open(self.path, "w").close()

#     def test_run_tests(self):
#         exercise = Exercise(path=self.path, interface=self.interface)

#         f = open(self.path, "w")
#         f.write("""
# def test_sth():
#     assert True == True
#         """)
#         f.close()

#         result_success = exercise.run_tests()
#         assert result_success.success == True
#         assert len(result_success.output) > 0 and isinstance(result_success.output, str)

#         f = open(self.path, "w")
#         f.write("""
# def test_sth():
#     assert True == False
#         """)
#         f.close()

#         result_success = exercise.run_tests()
#         assert result_success.success == False
#         assert len(result_success.output) > 0 and isinstance(result_success.output, str)

#         open(self.path, "w").close()

#     def test_check_done_comment(self):
#         exercise = Exercise(path=self.path, interface=self.interface)

#         f = open(self.path, "w")
#         f.write("print 'hello world'")
#         f.close()

#         result = exercise.check_done_comment()
#         assert result == False

#         f = open(self.path, "w")
#         f.write(
#             """

#                 # I AM NOT DONE

#                 print "hello world"

#                 """
#         )
#         f.close()

#         result = exercise.check_done_comment()
#         assert result == True

#         f = open(self.path, "w")
#         f.write("       ### I AM NOT DONE       ")
#         f.close()

#         result = exercise.check_done_comment()
#         assert result == True

#         open(self.path, "w").close()

#     def test_on_modified_recheck(self) -> None:
#         pass

#     def test_check_wait(self) -> bool:
#         pass

#     def test_watch_till_pass(self) -> str:
#         pass

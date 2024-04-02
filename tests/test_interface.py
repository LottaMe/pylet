from interface import Interface


class TestInterface:
    interface = Interface()

    def test_print_success(self, capsys) -> None:
        self.interface.print_success("yay")
        captured = capsys.readouterr()
        assert captured.out == "success: yay\n"

    def test_print_error(self, capsys) -> None:
        self.interface.print_error("nay")
        captured = capsys.readouterr()
        assert captured.out == "error: nay\n"

    def test_print_course_complete(self, capsys) -> None:
        self.interface.print_course_complete()
        captured = capsys.readouterr()
        assert captured.out == "You have completed the course!\n"

    def test_print_progress(self, capsys) -> None:
        all = ["1", "2", "3", "4", "5"]
        completed = ["1", "2"]

        self.interface.print_progress(all, completed)
        captured = capsys.readouterr()
        assert captured.out == "progress: ##>-- 2/5 40.0%" + "\n"

        all = ["1", "2"]
        completed = ["1", "2"]
        self.interface.print_progress(all, completed)
        captured = capsys.readouterr()
        assert captured.out == "progress: ## 2/2 100.0%" + "\n"

        all = ["1", "2", "3"]
        completed = ["1", "2"]
        self.interface.print_progress(all, completed)
        captured = capsys.readouterr()
        assert captured.out == "progress: ##> 2/3 66.7%" + "\n"

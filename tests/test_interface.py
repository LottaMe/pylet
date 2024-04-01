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

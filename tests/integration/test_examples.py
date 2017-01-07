from tests.base import BaseTest


class TestExamples(BaseTest):

    def test_folders(self, app):
        from examples.folders import example
        example(app.session_name)

    def test_scans(self, app):
        from examples.scans import example
        example(app.session_name, app.session_file_output)

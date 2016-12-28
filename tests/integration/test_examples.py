from tests.base import BaseTest


class TestExamples(BaseTest):

    def test_scans(self, app):
        from examples.scans import example
        example(app.session_name, app.session_file_output)

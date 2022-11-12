from app import app, models
from app.grouping import randomizer

def test_read_survey(mocker):
    config = models.Configuration('ser401', 1, 1, models.SurveyFieldMapping(
        "student_id",
        "student_name",
        "student_email_field_name",
        "student_login_field_name",
        "timezone_field_name",
        ["preferred_students_field_names"],
        ["disliked_students_field_names"],
        ["availability_field_names"]), models.ReportConfiguration(True, True, True), True, True, True)
    grouper = randomizer.RandomGrouper()
    
    application = app.Application(config, grouper)

    mocker.patch()
    application.read_survey("test.csv")
    
    
from requests import Session


class APIError(Exception):
    pass


def processing(func):
    def wrapper(self, arg):
        response = func(self, arg)
        try:
            return response.json()
        except:
            return response.text
    return wrapper
  

class APIBase:
    def __init__(self, token: str):
        self.host = 'https://api.school.mosreg.ru/'
        self.session = Session()
        self.session.headers = {"Access-Token": token}
    
    @processing
    def get(self, method: str, v: str = 'v2.0/'):
        return self.session.get(self.host + v + method)
    
    @processing
    def post(self, method: str, v: str = 'v2.0/'):
        return self.session.post(self.host + v + method)
    
    @processing
    def put(self, method: str, v: str = 'v2.0/'):
        return self.session.put(self.host + v + method)
    
    @processing
    def delete(self, method: str, v: str = 'v2.0/'):
        return self.session.delete(self.host + v + method)


class Client(APIBase):
    def __init__(self, token: str = None, login: str = None, password: str = None):
        self.token = token
        if login and password:
            self.token = self.get_token(login, password)
        if token:
            self.token = token
        super().__init__(self.token)

    def get_token(self, login, password):
        session = Session()
        data = {"exceededAttempts": "False", "ReturnUrl": "", "login": login, "password": password, "Captcha.Input": "", "Captcha.Id": ""}
        session.post("https://login.school.mosreg.ru/login", data=data)
        token = session.get(f'https://login.school.mosreg.ru/oauth2?response_type=token&client_id=bafe713c96a342b194d040392cadf82b&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo,SocialInfo&redirect_uri=').url
        if token[227:-53] == 'result=success':
            return token[255:-7]
        else:
            raise APIError('Неудачная авторизация')
    
    # Authorities

    def get_organizations(self):
        return self.get('users/me/organizations')
        
    def get_organization(self, organization_id):
        return self.get(f'users/me/organizations/{organization_id}')
    
    # Authorizations
    
    def post_code(self, data):
        return self.post('authorizations', data=data, v='')
    
    # AverageMarks
    
    def get_person_marks_for_period(self, person_id, period_id):
        return self.get(f'persons/{person_id}/reporting-periods/{period_id}/avg-mark')

    def get_person_marks_by_subject_for_period(self, person_id, period_id, subject_id):
        return self.get(f'persons/{person_id}/reporting-periods/{period_id}/subjects/{subject_id}/avg-mark')
    
    def get_group_marks_for_period_until_date(self, group_id, period_id, date):
        return self.get(f'edu-groups/{group_id}/reporting-periods/{period_id}/avg-marks/{date}')
    
    def get_group_marks_for_date_period(self, group_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/avg-marks/{from_date}/{to_date}')
    
    # Children
    
    def get_user_children(self, user_id):
        return self.get(f'users/{user_id}/children')
    
    def get_person_children(self, person_id):
        return self.get(f'persons/{person_id}/children')
    
    # Classmates
    
    def get_my_classmates(self):
        return self.get('users/me/classmates')
    
    def get_user_classmates(self, user_id):
        return self.get(f'users/{user_id}/classmates')
    
    # Context
    
    def get_user_context(self, user_id):
        return self.get(f'users/{user_id}/context')
    
    def get_my_context(self):
        return self.get('users/me/context')
    
    # CriteriaJournalMarks
    # None

    # EducationMemberships
    
    def get_user_school_memberships(self, user_id):
        return self.get(f'users/{user_id}/school-memberships')
    
    def get_user_education(self, user_id):
        return self.get(f'users/{user_id}/education')
    
    def get_user_schools(self, user_id):
        return self.get(f'users/{user_id}/schools')
    
    def get_user_groups(self, user_id):
        return self.get(f'users/{user_id}/edu-groups')

    def get_my_school_memberships(self):
        return self.get('users/me/school-memberships')
    
    def get_my_education(self):
        return self.get('users/me/education')
    
    def get_my_schools(self):
        return self.get('users/me/schools')
    
    def get_my_groups(self):
        return self.get('users/me/edu-groups')
    
    # EduGroups
    
    def get_group(self, group_id):
        return self.get(f'edu-groups/{group_id}')

    def get_school_groups(self, school_id):
        return self.get(f'schools/{school_id}/edu-groups')
    
    def get_person_groups(self, person_id):
        return self.get(f'persons/{person_id}/edu-groups')
    
    def get_person_school_groups(self, person_id, school_id):
        return self.get(f'persons/{person_id}/schools/{school_id}/edu-groups')
    
    def get_group_persons(self, group_id):
        return self.get(f'edu-groups/{group_id}/persons')
    
    def get_group_parallel(self, group_id):
        return self.get(f'edu-groups/{group_id}/parallel')
    
    def get_teacher_groups(self, person_id, school_id):
        return self.get(f'persons/{person_id}/schools/{school_id}/edu-groups/teacher')
    
    def post_group(self, data):
        return self.post('edu-groups', data=data)
    
    def post_group_students(self, data):
        return self.post('edu-groups/students', data=data)
    
    # EsiaAuthorization

    def post_esia_user(self, data):
        return self.post('authorizations/esia/v2.0/users/linked', data=data, v='')
    
    def post_esia(self, data):
        return self.post('authorizations/esia/v2.0', data=data, v='')

    # Files
    
    def get_folder_files(self, folder_id, page_number=1, page_size=10, order_by='id_asc'):
        return self.get(f'folder/{folder_id}/files', params={'page_number': page_number, 'page_size': page_size, 'order_by': order_by})
    
    def post_file_like(self, file_id):
        return self.post(f'files/{file_id}/like')

    def post_file_repost(self, file_id, text):
        return self.post(f'files/{file_id}/repost', params={'text': text})
    
    # FinalMarks
    
    def get_group_final_marks(self, group_id):
        return self.get(f'edu-groups/{group_id}/final-marks')
    
    def get_person_group_final_marks(self, person_id, group_id):
        return self.get(f'persons/{person_id}/edu-groups/{group_id}/final-marks')

    def get_person_group_all_final_marks(self, person_id, group_id):
        return self.get(f'persons/{person_id}/edu-groups/{group_id}/allfinalmarks')
    
    def get_group_subject_final_marks(self, group_id, subject_id):
        return self.get(f'edu-groups/{group_id}/subjects/{subject_id}/final-marks')
    
    # Friends
    
    def get_my_friends(self):
        return self.get('users/me/friends')
    
    def get_user_friends(self, user_id):
        return self.get(f'users/{user_id}/friends')
    
    # Homeworks
    
    def get_school_homework_for_date_period(self, school_id, start_date, end_date):
        return self.get(f'users/me/school/{school_id}/homeworks', params={'startDate': start_date, 'endDate': end_date})
    
    def get_homework(self, homework_id):
        return self.get(f'users/me/school/homeworks', params={'homeworkId': homework_id})
    
    def get_person_school_homework_for_date_period(self, person_id, school_id, start_date, end_date):
        return self.get(f'persons/{person_id}/school/{school_id}/homeworks', params={'startDate': start_date, 'endDate': end_date})
    
    # HomeworkTests

    def post_homework_test(self, work_id, data):
        return self.post(f'works/{work_id}/test', data=data)

    # LessonLog
    
    def delete_lesson_log(self, lesson_id, person_id):
        return self.delete(f'lessons/{lesson_id}/log-entries', params={'person': person_id})
    
    def get_lesson_log(self, lesson_id):
        return self.get(f'lessons/{lesson_id}/log-entries')
    
    def post_lesson_log(self, lesson_id, data):
        return self.post(f'lessons/{lesson_id}/log-entries', data=data)
    
    def put_lesson_log(self, lesson_id, data):
        return self.put(f'lessons/{lesson_id}/log-entries', data=data)

    def get_lesson_log_by_person(self, lesson_id, person_id):
        return self.get(f'lesson-log-entries/lesson/{lesson_id}/person/{person_id}')
    
    def get_group_lesson_log_by_subject_for_date_period(self, group_id, subject_id, from_date, to_date):
        return self.get(f'lesson-log-entries/group/{group_id}', params={'subject': subject_id, 'from': from_date, 'to': to_date})

    def get_person_lesson_log_by_subject_for_date_period(self, person_id, subject_id, from_date, to_date):
        return self.get(f'lesson-log-entries/person/{person_id}/subject/{subject_id}', params={'subject': subject_id, 'from': from_date, 'to': to_date})
    
    def get_person_lesson_log_for_date_period(self, person_id, start_date, end_date):
        return self.get(f'persons/{person_id}/lesson-log-entries', params={'startDate': start_date, 'endDate': end_date})
    
    # LessonLogStatuses
    
    def get_lesson_log_statuses(self):
        return self.get('lesson-log-entries/statuses')
    
    # Lessons
    
    def get_lesson(self, lesson_id):
        return self.get(f'lessons/{lesson_id}')
    
    def get_group_lessons_for_date_period(self, group_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/{from_date}/{to_date}')
    
    def get_group_lessons_by_subject_for_date_period(self, group_id, subject_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/subjects/{subject_id}/lessons/{from_date}/{to_date}')
    
    def post_lesson(self, data):
        return self.post('lessons', data=data)
    
    # MarkHistograms
    
    def get_histogram(self, work_id):
        return self.get(f'works/{work_id}/marks/histogram')
    
    def get_group_histogram_by_subject_for_period(self, group_id, subject_id, period_id):
        return self.get(f'periods/{period_id}/subjects/{subject_id}/groups/{group_id}/marks/histogram')
    
    # Marks
    
    def get_mark(self, mark_id):
        return self.get(f'marks/{mark_id}')
    
    def get_marks_by_work(self, work_id):
        return self.get(f'works/{work_id}/marks')
    
    def get_marks_by_lesson(self, lesson_id):
        return self.get(f'lessons/{lesson_id}/marks')
    
    def get_group_marks_for_date_period(self, group_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/marks/{from_date}/{to_date}')
    
    def get_group_marks_by_subject_for_date_period(self, group_id, subject_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/subjects/{subject_id}/marks/{from_date}/{to_date}')
    
    def get_person_school_marks_for_date_period(self, person_id, school_id, from_date, to_date):
        return self.get(f'persons/{person_id}/schools/{school_id}/marks/{from_date}/{to_date}')
    
    def get_person_group_marks_for_date_period(self, person_id, group_id, from_date, to_date):
        return self.get(f'persons/{person_id}/edu-groups/{group_id}/marks/{from_date}/{to_date}')

    def get_person_marks_by_lesson(self, person_id, lesson_id):
        return self.get(f'persons/{person_id}/lessons/{lesson_id}/marks')
    
    def get_person_marks_by_work(self, person_id, work_id):
        return self.get(f'persons{person_id}/works/{work_id}/marks')
    
    def get_person_marks_by_subject_for_date_period(self, person_id, subject_id, from_date, to_date):
        return self.get(f'persons/{person_id}/subjects/{subject_id}/marks/{from_date}/{to_date}')

    def get_person_marks_by_subject_group_for_date_period(self, person_id, subject_group_id, from_date, to_date):
        return self.get(f'persons/{person_id}/subject-groups/{subject_group_id}/marks/{from_date}/{to_date}')

    def get_person_marks_by_lesson_date(self, person_id, lesson_date):
        return self.get(f'lessons/{lesson_date}/persons/{person_id}/marks')
    
    def get_person_marks_by_date(self, person_id, date):
        return self.get(f'persons/{person_id}/marks/{date}')
    
    def post_mark(self, person_id, work_id):
        return self.post(f'persons/{person_id}/works/{work_id}/mark')

    # MarkValues
    
    def get_mark_values(self):
        return self.get('marks/values')
    
    def get_mark_type(self, type):
        return self.get(f'marks/values/type/{type}')
    
    # Persons
    
    def get_person(self, person_id):
        return self.get(f'persons/{person_id}')
    
    # PersonSchedules

    def get_person_schedule_by_snils(self, snils, since, till):
        return self.get('user/schedule', params={'snils': snils, 'since': since, 'till': till})

    # RecentMarks

    def get_person_group_recent_marks(self, person_id, group_id, from_date = None, subject_id = None, limit = None):
        params = {}
        if from_date != None:
            params['fromDate'] = from_date
        if subject_id != None:
            params['subject'] = subject_id
        if limit != None:
            params['limit'] = limit
        return self.get(f'persons/{person_id}/group/{group_id}/recentmarks', params=params)
    
    # Region
    
    def get_regions(self):
        return self.get('authorizations/esia/v2.0/regions', v='')
    
    # ReportingPeriods
    
    def get_group_periods(self, group_id):
        return self.get(f'edu-groups/{group_id}/reporting-periods')
    
    def get_group_period_group(self, group_id):
        return self.get(f'edu-groups/{group_id}/reporitng-period-groups')
    
    # Schedules
    
    def get_person_schedule_by_group_for_date_period(self, person_id, group_id, start_date, end_date):
        return self.get(f'persons/{person_id}/groups/{group_id}/shcedules', params={'startDate': start_date, 'endDate': end_date})
    
    # SchoolRating
    
    def get_school_rating_for_date_period(self, from_date, to_date):
        return self.get(f'school-rating/from/{from_date}/to/{to_date}')
    
    def get_new_school_rating_for_date_period(self, from_date, to_date):
        return self.get(f'school-rating/from/{from_date}/to/{to_date}/new')
    
    # Schools
    
    def get_school(self, school_id):
        return self.get(f'schools/{school_id}')
    
    def get_my_person_schools(self, exclude_organizations = False):
        return self.get('schools/person-schools', params={'excludeOrganizations': exclude_organizations})
    
    def get_school_cities(self):
        return self.get('schools/cities')
    
    def get_search_by_oktmo(self, oktmo):
        return self.get('schools/search/by-oktmo', params={'oktmo': oktmo})
    
    def get_school_membership(self, school_id, school_membership_type='Staff'):
        return self.get(f'schools/{school_id}/membership', params={'schoolMembershipType': school_membership_type})
    
    # SchoolsParameters
    
    def get_school_parameters(self, school_id):
        return self.get(f'schools/{school_id}/parameters')
    
    # SocialEvents
    
    def post_event_invite(self, id):
        return self.post(f'events/{id}/invite')
    
    # SocialGroups
    
    def post_group_invite(self, id):
        return self.post(f'groups/{id}/invite')
    
    # SocialNetworks
    
    def post_network_invite(self, id):
        return self.post(f'networks/{id}/invite')
    
    # Subjects
    
    def get_group_subjects(self, group_id):
        return self.get(f'edu-groups/{group_id}/subjects')
    
    def get_school_subjects(self, school_id):
        return self.get(f'schools/{school_id}/subjects')
    
    # Tasks
    
    def get_task(self, task_id):
        return self.get(f'tasks/{task_id}')
    
    def get_lesson_tasks(self, lesson_id):
        return self.get(f'lessons/{lesson_id}/tasks')
    
    def get_work_tasks(self, work_id, person_id):
        return self.get(f'works/{work_id}/tasks', params={'persons': person_id})
    
    def get_person_tasks_by_subject_for_date_period(self, person_id, subject_id, from_date, end_date, page_number=1, page_size=10):
        return self.get(f'persons/{person_id}/tasks', params={'subject': subject_id, 'fromDate': from_date, 'endDate': end_date, 'pageNumber': page_number, 'pageSize': page_size})
    
    def get_person_undone_tasks(self, person_id):
        return self.get(f'tasks/{person_id}/undone')
    
    # Teacher
    
    def get_teacher_students(self, teacher_user_id):
        return self.get(f'teacher/{teacher_user_id}/students')
    
    def get_school_teachers(self, school_id):
        return self.get(f'schools/{school_id}/teachers')
    
    def get_group_teachers(self, group_id):
        return self.get(f'edu-groups/{group_id}/teachers')
    
    # ThematicMarks
    
    def get_thematic_mark(self, mark_id):
        return self.get(f'thematic-marks/{mark_id}')
    
    def get_person_group_thematic_marks_by_subject_for_date_period(self, person_id, group_id, subject_id, from_date, to_date):
        return self.get(f'persons/{person_id}/edu-groups/{group_id}/subjects/{subject_id}/thematic-mmarks/{from_date}/{to_date}')
    
    def get_person_group_thematic_marks_for_date_period(self, person_id, group_id, from_date, to_date):
        return self.get(f'persons/{person_id}/edu-groups/{group_id}/thematic-marks/{from_date}/{to_date}')
    
    def get_person_school_thematic_marks_for_date_period(self, person_id, school_id, from_date, to_date):
        return self.get(f'persons/{person_id}/schools/{school_id}/thematic-marks/{from_date}/{to_date}')
    
    def get_group_thematic_marks_by_subject(self, group_id, subject_id):
        return self.get(f'edu-groups/{group_id}/subjects/{subject_id}/thematic-marks')
    
    def post_thematic_mark(self, data):
        return self.post('thematic-marks', data=data)
    
    # Timetables
    
    def get_school_timetable(self, school_id):
        return self.get(f'schools/{school_id}/timetables')
    
    def get_group_timetable(self, group_id):
        return self.get(f'edu-groups/{group_id}/timetables')
    
    # UserFeeds
    
    def get_user_feed(self, user_id):
        return self.get(f'users/{user_id}/feed')
    
    def get_my_feed(self):
        return self.get('users/me/feed')
    
    # UserGroups
    
    def get_user_groups(self, user_id):
        return self.get(f'users/{user_id}/groups')
    
    def get_my_groups(self):
        return self.get('users/me/groups')
    
    # UserRelatives
    
    def get_user_children(self, user_id):
        return self.get(f'users/{user_id}/children')

    def get_my_children(self):
        return self.get(f'users/me/children')

    def get_user_relatives(self, user_id):
        return self.get(f'users/{user_id}/relatives')

    def get_my_relatives(self):
        return self.get(f'users/me/relatives')

    def get_user_children_relatives(self, user_id):
        return self.get(f'users/{user_id}/childrenrelatives')

    def get_my_children_relatives(self):
        return self.get(f'users/me/childrenrelatives')
    
    # Users
    
    def get_user(self, user_id):
        return self.get(f'users/{user_id}')
    
    def get_me(self):
        return self.get('users/me')

    def get_user_roles(self, user_id):
        return self.get(f'users/{user_id}/roles')
    
    def get_my_roles(self):
        return self.get('users/me/roles')
    
    def post_user(self, data):
        return self.post('users', data=data)
    
    # UserWall
    
    def post_wall(self, user_id, data):
        return self.post(f'users/{user_id}/wallrecord', data=data)
    
    # WeightedAverageMarks
    
    def get_group_weighted_average_marks_for_date_period(self, group_id, from_date, to_date):
        return self.get(f'edu-groups/{group_id}/wa-marks/{from_date}/{to_date}')
    
    # Works
    
    def get_lesson_works(self, lesson_id):
        return self.get('works', params={'lesson': lesson_id})
    
    def post_work(self, data):
        return self.post('works', data=data)
    
    def delete_work(self, work_id):
        return self.delete(f'works/{work_id}')
    
    def put_work(self, work_id, data):
        return self.put(f'works/{work_id}', data=data)
    
    def post_person_work_status(self, person_id, work_id):
        return self.post(f'works/{work_id}/persons/{person_id}/status')
    
    # WorkTypes
    
    def get_school_work_types(self, school_id):
        return self.get(f'work-types/{school_id}')

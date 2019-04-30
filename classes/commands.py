from ta_assign import models


class Commands:

    # commands organized by page menu order

    # Login commands
    # this appears to be unused in the view
    @staticmethod
    def login(email, password):

        people = models.User.objects.all()

        temp = None

        for i in people:
            if i.isLoggedOn is True:
                return "User already logged in"
            if i.email == email:
                temp = i

        if temp is None:
            return "Invalid login info"
        elif temp.email != email or temp.password != password:
            return "Invalid login info"
        models.User.objects.filter(email=email).update(isLoggedOn=True)
        return

    # Logout commands
    # this also appears unused in the view
    @staticmethod
    def logout(email):

        person = models.User.objects.get(email=email)
        if person.isLoggedOn is False:
            return False
        models.User.objects.filter(email=email).update(isLoggedOn=False)
        return True

    # Create Account Commands
    @staticmethod
    def create_account(email, password, account_type):
        # Jeff's method
        # Usage: (string: email, string: password, string: account_type)
        # returns True if account successfully created in DB
        # returns False if account was unable to be created
        # throws exceptions if you do it wrong

        try:
            find_email = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            find_email = "none"

        if find_email != "none":
            return "Email address taken."

        parse_at = email.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return "Email address must be uwm address."
        # I'm not sure why I wrote this exception, I don't test for it and can't
        # figure out how it'd even show up, but if it does someday, we'll find out
        except IndexError:
            return "Bad email address."

        if password == "":
            return "Bad password."

        if account_type != "instructor" and account_type != "ta":
            return "Invalid account type."

        some_guy = models.User()
        some_guy.email = email
        some_guy.password = password
        some_guy.type = account_type
        some_guy.save()

        return "Account created!"

    # Create Course Commands

    # Access Info Commands

    # Edit Account Commands

    # Edit Info Commands

    # Assign Instructor Commands
    @staticmethod
    def assign_instructor(email, course):
        try:
            check_ins = models.User.objects.get(email=email, type="instructor")
        except models.User.DoesNotExist:
            check_ins = None
        if check_ins is None:
            return "no such instructor"
        try:
            check_course = models.Course.objects.get(course_id=course)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        models.Course.objects.filter(course_id=course).update(instructor=email)

        return "Instructor Assigned!"

    # Assign TA Commands
    @staticmethod
    def assign_ta(email, course):
        try:
            check_ta = models.User.objects.get(email=email, type="ta")
        except models.User.DoesNotExist:
            check_ta = None
        if check_ta is None:
            return "no such ta"
        try:
            check_course = models.Course.objects.get(course_id=course)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        ta_course = models.TACourse()
        ta_course.TA = check_ta
        ta_course.course = check_course
        ta_course.save()
        return "TA Assigned"
    # View TA Assign Commands

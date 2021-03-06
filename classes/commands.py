from ta_assign import models
import time


class Commands:

    # commands organized by page menu order

    # Login commands
    # this appears to be unused in the view
    @staticmethod
    def login(email, password):

        people = models.User.objects.all()

        temp = None

        for i in people:
            if i.email == email:
                temp = i

        if temp is None:
            return "Invalid login info"
        elif temp.email != email or temp.password != password:
            return "Invalid login info"
        models.User.objects.filter(email=email).update(isLoggedOn=True)
        return "Login successful"

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

        if len(email) > 50:
            return "Email address must be 50 characters or less."

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

        if len(password) > 20:
            return "Password must be 20 characters or less."

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
    @staticmethod
    def create_course(department, course_id, num_lectures, num_labs):
        good_dept = ["COMPSCI", "ELECENG", "PHYSICS", "MATH", "BIOMED", "CIVIL", "INDENG", "MATENG",
                     "MECHENG", "STRUCENG", "WEBDEV"]
        if department not in good_dept:
            return "That department is not offered"
        if not course_id.isdigit():
            return "Course ID must be a number"
        if int(course_id) < 101 or int(course_id) > 999:
            return "Course ID must be 3 digits long and between 101 and 999"
        if not num_labs.isdigit():
            return "Number of lab sections must be a number"
        if not num_lectures.isdigit():
            return "Number of lecture sections must be a number"
        if int(num_labs) < 0 or int(num_labs) > 5:
            return "Number of lab sections cannot be less than 0 or greater than 5"
        if int(num_lectures) < 1 or int(num_lectures) > 5:
            return "Number of lecture sections cannot be less than 1 or greater than 5"

        try:
            find_course = models.Course.objects.get(course_department=department, course_id=course_id)
        except models.Course.DoesNotExist:
            find_course = "none"
        if find_course != "none":
            return "Course already exists"

        some_course = models.Course()
        some_course.course_department = department
        some_course.course_id = course_id
        some_course.course_dept_id = department + str(course_id)
        some_course.num_lectures = num_lectures
        some_course.num_labs = num_labs
        some_course.save()

        for i in range(int(num_labs)):
            lab = models.Lab()
            lab.lab_section = 801 + i
            lab.course = some_course
            lab.save()

        for i in range(int(num_lectures)):
            lec = models.Lecture()
            if int(num_labs) == 0:
                temp = 1+i
                lec.lecture_section = "00" + str(temp)
            else:
                lec.lecture_section = 401 + i
            lec.course = some_course
            lec.save()

        return "Course created successfully"

    # Access Info Commands
    @staticmethod
    def access_info():
        # Jeff's method
        # Usage: access_info()
        # returns a list with two lists, one with all users, the other with all courses
        # from there, it's up to something else to format it
        stuff = []
        users = models.User.objects.all()
        courses = models.Course.objects.all()
        stuff.append(users)
        stuff.append(courses)

        return stuff

    # Edit Account Commands
    @staticmethod
    def edit_account(email, field, content):
        try:
            models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return "Entered user does not exist"

        if field == "email":
            parse_at = content.split("@")
            try:
                if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                    return "Entered email does not end in uwm.edu"
            except ValueError:
                return "Entered email is not of the correct form"
            models.User.objects.filter(email=email).update(email=content)
            return "User has been updated successfully"

        elif field == "password":
            models.User.objects.filter(email=email).update(password=content)
            return "User has been updated successfully"

        elif field == "phone":
            parse_phone = content.split(".")
            if len(parse_phone) != 3:
                return "Phone number is not of the correct form (###.###.####)"
            if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
                return "Phone number is not of the correct form (###.###.####)"
            if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
                return "Phone number is not of the correct form (###.###.####)"
            models.User.objects.filter(email=email).update(phone=content)
            return "User has been updated successfully"

        elif field == "name":
            models.User.objects.filter(email=email).update(name=content)
            return "User has been updated successfully"
        elif field == "address":
            models.User.objects.filter(email=email).update(address=content)
            return "User has been updated successfully"
        else:
            return "The entered data field does not exist"

    @staticmethod
    def edit_lec_lab(department, course_id, section_type, section_id, location, sectime):
        good_dept = ["COMPSCI", "ELECENG", "PHYSICS", "MATH", "BIOMED", "CIVIL", "INDENG", "MATENG",
                     "MECHENG", "STRUCENG", "WEBDEV"]
        if department not in good_dept:
            return "That department is not offered"
        if not course_id.isdigit():
            return "Course ID must be a number"
        if int(course_id) < 101 or int(course_id) > 999:
            return "Course ID must be 3 digits long and between 101 and 999"
        if not section_id.isdigit():
            return "Section ID must be a number"
        if len(section_id) != 3:
            return "Section ID must be 3 digits long"
        if int(section_id) < 1 or int(section_id) > 999:
            return "Section ID must be between 001 and 999"
        try:
            course = models.Course.objects.get(course_department=department, course_id=course_id)
        except models.Course.DoesNotExist:
            return "That course does not exist"
        if section_type == "lecture":
            try:
                models.Lecture.objects.get(course=course, lecture_section=section_id)
            except models.Lecture.DoesNotExist:
                return "That lecture does not exist"
            lecture = models.Lecture.objects.filter(course=course, lecture_section=section_id)
            if location != "":
                lecture.update(lecture_location=location)
            if sectime != "":
                try:
                    time.strptime(sectime, '%H:%M')
                except ValueError:
                    return "Bad time format (HH:MM)"
                lecture.update(lecture_time=sectime)
        elif section_type == "lab":
            try:
                models.Lab.objects.get(course=course, lab_section=section_id)
            except models.Lab.DoesNotExist:
                return "That lab does not exist"
            lab = models.Lab.objects.filter(course=course, lab_section=section_id)
            if location != "":
                lab.update(lab_location=location)
            if sectime != "":
                try:
                    time.strptime(sectime, '%H:%M')
                except ValueError:
                    return "Bad time format (HH:MM)"
                lab.update(lab_time=sectime)
        else:
            return "Invalid section type"
        return "Section has been edited successfully."

    # Edit Info Commands
    @staticmethod
    def change_password(email, new):
        if new == "":
            return "Bad password."

        if len(new) > 20:
            return "Password must be 20 characters or less."

        models.User.objects.filter(email=email).update(password=new)
        return "Password changed."

    @staticmethod
    def change_email(email, address):

        if len(address) > 50:
            return "Email address must be 50 characters or less."

        parse_at = address.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return "Email address must be uwm address."
        except ValueError:
            return "Bad email address."

        try:
            find_email = models.User.objects.get(email=address)
        except models.User.DoesNotExist:
            find_email = "none"

        if find_email != "none":
            return "Email address taken."

        models.User.objects.filter(email=email).update(email=address)
        return "Email address changed."

    @staticmethod
    def change_name(email, name):
        if len(name) > 50:
            return "Name must be 50 characters or less."

        if name == "":
            return "Bad name."

        models.User.objects.filter(email=email).update(name=name)
        return "Name changed."

    @staticmethod
    def change_phone(email, phone):
        parse_phone = phone.split(".")
        invalid = "Invalid phone format."
        if len(parse_phone) != 3:
            return invalid
        if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
            return invalid
        if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
            return invalid

        models.User.objects.filter(email=email).update(phone=phone)
        return "Phone number changed."

    @staticmethod
    def change_address(email, address):
        if len(address) > 100:
            return "Address must be 100 characters or less."

        if address == "":
            return "Bad address."

        models.User.objects.filter(email=email).update(address=address)
        return "Address changed."

    # View Info Commands
    @staticmethod
    def view_info(email):

        this_guy = models.User.objects.get(email=email)
        info_list = [this_guy.email, this_guy.password, this_guy.name, this_guy.phone, this_guy.address]

        return info_list

    # Assign Instructor Commands
    @staticmethod
    def assign_instructor_to_course(email, course_id, course_department):
        try:
            check_ins = models.User.objects.get(email=email, type="instructor")
        except models.User.DoesNotExist:
            check_ins = None
        if check_ins is None:
            return "no such instructor"
        try:
            check_course = models.Course.objects.get(course_id=course_id, course_department=course_department)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        else:
            try:
                check_exist = models.InstructorCourse.objects.get(course=check_course, instructor=check_ins)
            except models.InstructorCourse.DoesNotExist:
                check_exist = None

            if check_exist is None:
                numins = check_course.current_num_lectures
                if numins+1 > check_course.num_lectures:
                    return "Too Many Instructors Assigned"
                models.Course.objects.filter(course_id=course_id, course_department=course_department).\
                    update(current_num_lectures=numins+1)
                ins_course = models.InstructorCourse()
                ins_course.course = check_course
                ins_course.instructor = check_ins
                ins_course.save()
                return "Instructor Assigned!"
            else:
                return "Instructor Already Assigned!"

    # Assign TA Commands
    @staticmethod
    def assign_ta_to_course(email, course_id, course_department):
        try:
            check_ta = models.User.objects.get(email=email, type="ta")
        except models.User.DoesNotExist:
            check_ta = None
        if check_ta is None:
            return "no such ta"
        try:
            check_course = models.Course.objects.get(course_id=course_id, course_department=course_department)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        else:
            try:
                check_exist = models.TACourse.objects.get(course=check_course, TA=check_ta)
            except models.TACourse.DoesNotExist:
                check_exist = None

            if check_exist is None:
                numta = check_course.current_num_TA
                numlec = check_course.num_lectures
                if check_course.num_labs != 0 and numta+1 > check_course.num_labs:
                    return "Too Many TA's Assigned"
                elif numta+1 > numlec and check_course.num_labs == 0:
                    return "Too Many TA's Assigned"
                models.Course.objects.filter(course_id=course_id, course_department=course_department).\
                    update(current_num_TA=numta+1)
                ta_course = models.TACourse()
                ta_course.TA = check_ta
                ta_course.course = check_course
                ta_course.save()
                return "TA Assigned!"
            else:
                return "TA Already Assigned!"

    @staticmethod
    def assign_instructor_to_lec(email, course_id, course_section, course_department):
        try:
            check_ins = models.User.objects.get(email=email, type="instructor")
        except models.User.DoesNotExist:
            check_ins = None
        if check_ins is None:
            return "no such instructor"
        try:
            check_course = models.Course.objects.get(course_id=course_id, course_department=course_department)
        except models.Course.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"
        try:
            check_exist = models.InstructorCourse.objects.get(course=check_course, instructor=check_ins)
        except models.InstructorCourse.DoesNotExist:
            check_exist = None
        if check_exist is None:
            return "Instructor not assigned to this course!"
        try:
            check_lec = models.Lecture.objects.get(course=check_course, lecture_section=course_section)
        except models.Lecture.DoesNotExist:
            check_lec = None
        if check_lec is None:
            return "Lecture section does not exist"
        models.Lecture.objects.filter(course=check_course, lecture_section=course_section).update(instructor=email)
        return "Instructor assigned to lecture"

    # View course assignments
    @staticmethod
    def view_course_assignments(instructor):
        string_list = ""
        ins = models.User.objects.get(email=instructor)
        courses = models.InstructorCourse.objects.filter(instructor=ins)
        for course in courses:
            string_list = string_list + course.course.course_department+": "+ str(course.course.course_id) + " \n"

        return string_list

    @staticmethod
    def assign_ta_to_lablec(assigner, email, course_id, course_section, course_department):
        try:
            inst = models.User.objects.get(email=assigner, type="instructor")
        except models.User.DoesNotExist:
            inst = None
        if inst is not None:
            try:
                check_course = models.Course.objects.get(course_id=course_id, course_department=course_department)
            except models.Course.DoesNotExist:
                check_course = None
            if check_course is None:
                return "no such course"
            try:
                valid = models.InstructorCourse.objects.get(course=check_course, instructor=inst)
            except models.InstructorCourse.DoesNotExist:
                valid = None
            if valid is None:
                return "You are not assigned to this course"
            try:
                check_ta = models.User.objects.get(email=email, type="ta")
            except models.User.DoesNotExist:
                check_ta = None
            if check_ta is None:
                return "no such ta"
            try:
                check_exist = models.TACourse.objects.get(course=check_course, TA=check_ta)
            except models.TACourse.DoesNotExist:
                check_exist = None
            if check_exist is None:
                return "TA not assigned to this course!"
            try:
                check_lec = models.Lecture.objects.get(course=check_course, lecture_section=course_section)
            except models.Lecture.DoesNotExist:
                check_lec = None
            if check_lec is not None:
                if check_course.num_labs is not 0:
                    return "TA cannot be assigned to this lecture(labs exist)!"
                models.Lecture.objects.filter(course=check_course, lecture_section=course_section).update(TA=email)
                return "TA Assigned to Lecture!"

            try:
                check_lab = models.Lab.objects.get(course=check_course, lab_section=course_section)
            except models.Lab.DoesNotExist:
                return "No Such Lab or Lecture"
            models.Lab.objects.filter(course=check_course, lab_section=course_section).update(TA=email)
            return "TA Assigned to Lab!"
        else:
            inst = models.User.objects.get(email=assigner, type="supervisor")
            try:
                check_course = models.Course.objects.get(course_id=course_id, course_department=course_department)
            except models.Course.DoesNotExist:
                check_course = None
            if check_course is None:
                return "no such course"
            try:
                check_ta = models.User.objects.get(email=email, type="ta")
            except models.User.DoesNotExist:
                check_ta = None
            if check_ta is None:
                return "no such ta"
            try:
                check_exist = models.TACourse.objects.get(course=check_course, TA=check_ta)
            except models.TACourse.DoesNotExist:
                check_exist = None
            if check_exist is None:
                return "TA not assigned to this course!"
            try:
                check_lec = models.Lecture.objects.get(course=check_course, lecture_section=course_section)
            except models.Lecture.DoesNotExist:
                check_lec = None
            if check_lec is not None:
                if check_course.num_labs is not 0:
                    return "TA cannot be assigned to this lecture(labs exist)!"
                models.Lecture.objects.filter(course=check_course, lecture_section=course_section).update(TA=email)
                return "TA Assigned to Lecture!"
            else:
                try:
                    check_lab = models.Lab.objects.get(course=check_course, lab_section=course_section)
                except models.Lab.DoesNotExist:
                    return "No Such Lab or Lecture"
                models.Lab.objects.filter(course=check_course, lab_section=course_section).update(TA=email)
                return "TA Assigned to Lab!"
    # View TA Assign Commands

    @staticmethod
    def view_ta_assign():
        string_list = ""
        tas = models.User.objects.filter(type="ta")
        for ta in tas:
            string_list = string_list + "TA: " + ta.name + " | " + ta.email + " | " + ta.phone + "\n"

            for ta_courses in models.TACourse.objects.all():
                if ta_courses.TA.email == ta.email:
                    string_list = string_list + "\tCourse: " + ta_courses.course.course_dept_id + "\n"

            for ta_lec in models.Lecture.objects.all():
                if ta_lec.TA == ta.email:
                    string_list = string_list + "\tLec-Section: " + ta_lec.lab_section + " Location: " +\
                                    ta_lec.lab_location + " Time: " + str(ta_lec.lab_time) + "\n"

            for ta_lab in models.Lab.objects.all():
                if ta_lab.TA == ta.email:
                    string_list = string_list + "\tLab-Section: " + ta_lab.lab_section + " Location: " +\
                                ta_lab.lab_location + " Time: " + str(ta_lab.lab_time) + "\n"
            string_list = string_list + "\n"

        return string_list

    # Read Public Contact Info Commands
    @staticmethod
    # returns a list with all the users
    # it's up to the view to format this nicely
    def read_public():
        users = models.User.objects.all()
        return users

    # Delete Account
    @staticmethod
    def delete_account(email):

        people = models.User.objects.filter(email=email)

        if len(people) != 1:
            return "Such User does not exist"
        person = people[0]
        if person.type == "administrator" or person.type == "supervisor":
            return "You cannot delete this account"
        if person.type == "TA":
            models.Lab.objects.filter(TA=person.email).update(TA="no TA")
        if person.type == "instructor":
            models.Lecture.objects.filter(instructor=person.email).update(instructor="no instructor")

        models.User.objects.filter(email=person.email).delete()

        return email+" has been deleted successfully"


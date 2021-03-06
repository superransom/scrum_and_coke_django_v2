"""scrum_and_coke_django_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from ta_assign.views import Index, Login, Logout, CreateAccount, AccessInfo, CreateCourse, EditAccount, EditInfo,\
    EditLecLab, AssignInstructorToCourse, AssignTAToCourse, ViewCourseAssignments, CourseView, AssignTAToLabLec,\
    AssignInstructorToLecture, InstructorView, ViewTAAssign, TAView, DeleteAccount, ContactInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index1'),
    path('index/', Index.as_view(), name='index1'),
    path('login/', Login.as_view(), name='Login1'),
    path('logout/', Logout.as_view(), name='Logout1'),
    path('create_account/', CreateAccount.as_view(), name='CreateAccount1'),
    path('create_course/', CreateCourse.as_view(), name='CreateCourse1'),
    path('access_info/', AccessInfo.as_view(), name='AccessInfo1'),
    path('edit_account/', EditAccount.as_view(), name='EditAccount1'),
    path('edit_lec_lab/', EditLecLab.as_view(), name='EditLecLab1'),
    path('assign_ta/', AssignTAToCourse.as_view(), name='AssignTACourse1'),
    path('assign_instructor/', AssignInstructorToCourse.as_view(), name='AssignInstructor1'),
    path('assign_ta_lablec/', AssignTAToLabLec.as_view(), name='AssignTALabLec1'),
    path('assign_instructor_lec/', AssignInstructorToLecture.as_view(), name='AssignInstructorLec1'),
    path('view_course_assignments/', ViewCourseAssignments.as_view(), name='ViewCourseAssignments1'),
    path('edit_info/', EditInfo.as_view(), name='EditInfo1'),
    path('view_ta_assign/', ViewTAAssign.as_view(), name='ViewTAAssign1'),
    path('delete_account/', DeleteAccount.as_view(), name='Delete1'),
    url(r'^course/(?P<course_dept_id>.+?)/$', CourseView.as_view(), name='Course1'),
    url(r'^instructor/(?P<instructor_email>.+?)/$', InstructorView.as_view(), name='Instructor1'),
    url(r'^ta/(?P<ta_email>.+?)/$', TAView.as_view(), name='TA1'),
    path('contact_info/', ContactInfo.as_view(), name='ContactInfo1')
]

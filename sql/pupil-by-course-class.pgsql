--- pupils by course/class ---
select
    crs.name as class_name,
    s.firstname, s.lastname,
    g.target,
    g.working,
    g.target_aspirational
from course crs
    inner join students_courses scrs on crs.id = scrs.course_id
    inner join student s on s.id = scrs.student_id
    inner join grade g on g.id = scrs.grade_id

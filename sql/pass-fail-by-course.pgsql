
--- pass/fail by course ---
SELECT
    i.course,
    i.level,
    i.pass,
    i.fail,
    i.unknown,
    i.total_pupils,
    ROUND(((i.pass::float / total_pupils::float)*100)::float) as pct_pass,
    ROUND(((i.fail / total_pupils::float)*100)::float) as pct_fail,
    ROUND(((i.unknown / total_pupils::float)*100)::float) as pct_unknown,
    i.avg_working,
    i.avg_target,
    i.avg_target_aspirational
FROM (
    SELECT
        c.name as course,
        l.name as "level",
        SUM(
            case
                when g.working >= 1 and g.working <= 6 then 1
                else
                    0
            end
        ) as pass,
        SUM(
            case
                when g.working > 6 then 1
                else
                    0
            end
        ) as fail,
        SUM(
            case
                when g.working is NULL then 1
                else
                    0
            end
        ) as unknown,
        COUNT(*) AS total_pupils,
        ROUND(AVG(g.working), 2) as avg_working,
        ROUND(AVG(g.target), 2) as avg_target,
        ROUND(AVG(g.target_aspirational), 2) as avg_target_aspirational

    from students_courses sc
        inner join grade g on g.id = sc.grade_id
        inner join course c on c.id = sc.course_id
        inner join levels_courses lc on lc.course_id = c.id
        inner join level l on l.id = lc.level_id
    WHERE
        l.name = 'NAT'
    group by
        "course",
        "level"
    order by c.name desc
) i

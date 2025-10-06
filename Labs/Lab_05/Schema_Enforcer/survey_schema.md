| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `student_id` | `INT` | Unique identifier for the student. |
| `major` | `VARCHAR[45]` | The student's declared academic major |
| `GPA` | `FLOAT` | The student's grade point average on 4.0 scale  |
| `is_cs_major` | `BOOLEAN` | indicates whether the student's major is Computer Science |
| `credits_taken` | `FLOAT` | The total number of academic credits that the student has completed |

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `name` | `VARCHAR[45]` | The name of the instructor or staff member associated with the course |
| `role` | `VARCHAR[30]` | The role of the person in the course |
| `course_id` | `VARCHAR[20]` | The unique identifier for the course  |
| `section` | `INT` | The numeric section identifier for the course |
| `title` | `VARCHAR[60]` | The full title of the course |
| `level` | `INT` | The course level or academic classification |
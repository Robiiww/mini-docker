CREATE TABLE Timetable (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(255),
    day VARCHAR(50),
    time VARCHAR(50),
    room VARCHAR(50),
    level INT
);

INSERT INTO Timetable (id, course_name, day, time, room, level) VALUES
(1,'Introduction to Computer Science', 'Monday', '9:00 AM', 'Room 101', 1),
(2,'Operating Systems', 'Tuesday', '10:00 AM', 'Room 202', 2),
(3,'Database Management Systems', 'Wednesday', '1:00 PM', 'Room 303', 2),
(4,'Data Structures and Algorithms', 'Thursday', '11:00 AM', 'Room 204', 3),
(5,'Machine Learning', 'Friday', '2:00 PM', 'Room 305', 3);
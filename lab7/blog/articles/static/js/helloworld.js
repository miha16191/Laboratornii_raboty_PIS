const groupmates = [
    {
        name: "Александр",
        surname: "Иванов",
        group: "БВТ1702",
        marks: [4, 3, 5]
    },
    {
        name: "Иван",
        surname: "Петров",
        group: "БСТ1702",
        marks: [4, 4, 4]
    },
    {
        name: "Кирилл",
        surname: "Смирнов",
        group: "БВТ1702",
        marks: [5, 5, 5]
    },
    {
        name: "Анна",
        surname: "Соколова",
        group: "БВТ1702",
        marks: [5, 4, 5]
    },
    {
        name: "Мария",
        surname: "Кузнецова",
        group: "БСТ1702",
        marks: [3, 4, 3]
    }
];


function rpad(value, length) {
    let text = String(value);

    while (text.length < length) {
        text = text + " ";
    }

    return text;
}


function averageMark(student) {
    let sum = 0;

    for (let i = 0; i < student.marks.length; i++) {
        sum = sum + student.marks[i];
    }

    return sum / student.marks.length;
}


function printStudents(students) {
    console.log(
        rpad("Имя", 15) +
        rpad("Фамилия", 15) +
        rpad("Группа", 12) +
        rpad("Оценки", 16) +
        "Средний балл"
    );

    for (let i = 0; i < students.length; i++) {
        const student = students[i];

        console.log(
            rpad(student.name, 15) +
            rpad(student.surname, 15) +
            rpad(student.group, 12) +
            rpad(student.marks.join(", "), 16) +
            averageMark(student).toFixed(2)
        );
    }

    if (students.length === 0) {
        console.log("Подходящих студентов нет.");
    }
}


console.log("Исходный массив:");
console.log(groupmates);

console.log("Все студенты:");
printStudents(groupmates);

function filterByGroup(students, groupName) {
    return students.filter(function (student) {
        return student.group === groupName;
    });
}


function filterByAverage(students, threshold) {
    return students.filter(function (student) {
        return averageMark(student) > threshold;
    });
}

function runFilters() {
    const groupInput = prompt("Введите группу, например БВТ1702:");

    if (groupInput === null) {
        return;
    }

    const groupName = groupInput.trim().toUpperCase();

    if (groupName === "") {
        console.log("Название группы не введено.");
        return;
    }

    console.log("Студенты группы " + groupName + ":");
    printStudents(filterByGroup(groupmates, groupName));

    const averageInput = prompt("Введите порог среднего балла:");

    if (averageInput === null) {
        return;
    }

    const normalizedInput = averageInput.trim().replace(",", ".");
    const threshold = Number(normalizedInput);

    if (normalizedInput === "" || !Number.isFinite(threshold)) {
        console.log("Нужно ввести число, например 4 или 4.5.");
        return;
    }

    console.log("Студенты со средним баллом выше " + threshold + ":");
    printStudents(filterByAverage(groupmates, threshold));
}
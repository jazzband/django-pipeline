type FullName = string;

interface User {
    firstName: string;
    lastName: string;
}


function getName(u: User): FullName {
    return `${u.firstName} ${u.lastName}`;
}

let userName: FullName = getName({firstName: "Django", lastName: "Pipeline"});

function getName(u) {
    return "".concat(u.firstName, " ").concat(u.lastName);
}
var userName = getName({ firstName: "Django", lastName: "Pipeline" });

class Usuario {
    constructor(nombre, apellido,edad, email, celular, direccion,plan) {
        this._nombre = nombre;
        this._apellido = apellido;
        this._edad = edad;
        this._email = email;
        this._celular = celular;
        this._direccion = direccion;
        this._plan = plan;
    }
    get nombre() {
        return this._nombre;
    }
    set nombre(nombre) {
        this._nombre = nombre;
    }
    get apellido() {
        return this._apellido;
    }
    set apellido(apellido) {
        this._apellido = apellido;
    }
    get edad() {
        return this._edad;
    }
    set edad(edad) {
        this._edad = edad;
    }
    get email() {
        return this._email;
    }
    set email(email) {
        this._email = email;
    }
    get celular() {
        return this._celular;
    }
    set celular(celular) {
        this._celular = celular;
    }
    get direccion() {
        return this._direccion;
    }
    set direccion(direccion) {
        this._direccion = direccion;
    }
    get plan() {
        return this._plan;
    }
    set plan(plan) {
        this._plan = plan;
    }
}
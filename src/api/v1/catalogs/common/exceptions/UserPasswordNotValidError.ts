export default class UserPasswordNotValidError extends Error {
    get name() {
        return 'UserPasswordNotValidError';
    }
}
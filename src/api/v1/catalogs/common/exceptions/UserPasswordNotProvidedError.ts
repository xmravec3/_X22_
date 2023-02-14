export default class UserPasswordNotProvidedError extends Error {
    get name() {
        return 'UserPasswordNotProvidedError';
    }
}
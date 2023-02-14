export default class UserLastNameNotProvidedError extends Error {
    get name() {
        return 'UserLastNameNotProvidedError';
    }
}
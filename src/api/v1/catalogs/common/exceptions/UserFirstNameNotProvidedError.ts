export default class UserFirstNameNotProvidedError extends Error {
    get name() {
        return 'UserFirstNameNotProvidedError';
    }
}
export default class UserNotPermittedError extends Error {
    get name() {
        return 'UserNotPermittedError';
    }
}
export default class RegistrationKeyNotExistsError extends Error {
    get name() {
        return 'RegistrationKeyNotExistsError';
    }
}
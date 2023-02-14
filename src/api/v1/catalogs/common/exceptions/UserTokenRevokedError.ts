export default class UserTokenRevokedError extends Error {
    get name() {
        return 'UserTokenRevokedError';
    }
}
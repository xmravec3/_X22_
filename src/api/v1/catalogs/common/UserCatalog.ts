import { User, UserType } from './domains/User';
import IUserCatalog from './interfaces/IUserCatalog';
import Catalog from '../../../common/catalogs/Catalog';
import IPassword from '../../security/interfaces/IPassword';
import UserTokenRevokedError from './exceptions/UserTokenRevokedError';

export default class UserCatalog extends Catalog implements IUserCatalog {

    async getByID(id: number, userType: UserType): Promise<User> {
        const sql = `
            SELECT 
                user.ID as id, 
                login, 
                name,
                email
            FROM user 
            INNER JOIN user_2_user_type ON  user.ID = user_2_user_type.user_ID 
                                        AND user_2_user_type.user_type_ID = ? 
            WHERE user.ID = ?;
        `.replace(/\s+|\n/g, ' ')

        return this._getOne(this._toUsers(await Catalog.getConnector().query({ query: sql, bindings: [userType, id] })));
    }

    async getByLogin(login: string, userType: UserType): Promise<User> {
        const sql = `
            SELECT 
                user.ID as id, 
                login, 
                name,
                email
            FROM user
            INNER JOIN user_2_user_type ON  user.ID = user_2_user_type.user_ID 
                                        AND user_2_user_type.user_type_ID = ? 
            WHERE login = ?;
        `.replace(/\s+|\n/g, ' ');

        return this._getOne(this._toUsers(await Catalog.getConnector().query({ query: sql, bindings: [userType, login] })));
    }

    async getByCredentials(login: string, password: IPassword, userType: UserType): Promise<User> {
        const sql = `
            SELECT 
                user.ID as id, 
                login, 
                name,
                email,
                password,
                permissions
            FROM user 
            INNER JOIN user_2_user_type ON  user.ID = user_2_user_type.user_ID 
                                        AND user_2_user_type.user_type_ID = ? 
            WHERE login = ?;
        `.replace(/\s+|\n/g, ' ');

        const user = this._getOne(this._toUsers(await Catalog.getConnector().query({ query: sql, bindings: [userType, login] })));

        if (await password.validate(String(user.password))) {
            delete user.password; // clear the password and get it secure

            return user;
        }

        throw new Error('User not found!')
    }

    async getByToken(id: number, token: string): Promise<User> {
        return this._getOne(this._toUsers(await Catalog.getConnector().query({ query: 'SELECT u.`ID` as id, u.`login`, u.`name`, u.`email`, ut.`token`, ut.`revoked` as `token_revoked` FROM user u INNER JOIN user_token ut ON u.ID = ut.user_ID AND ut.token = ? WHERE u.ID = ?;', bindings: [token, id] })));
    }

    async saveToken(id: number, token: string): Promise<void> {
        return Catalog.getConnector().query({ query: 'INSERT INTO user_token (`user_ID`, `token`) VALUES (?, ?);', bindings: [id, token] });
    }

    async deleteToken(id: number, token: string): Promise<void> {
        return Catalog.getConnector().query({ query: 'DELETE FROM user_token WHERE user_ID = ? AND token = ?;', bindings: [id, token] });
    }

    async deleteAllTokens(id: number): Promise<void> {
        return Catalog.getConnector().query({ query: 'DELETE FROM user_token WHERE user_ID = ?;', bindings: [id] });
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toUsers(result: any): User[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((user: any) => user);
    }

    private _getOne(users: User[]): User {
        if (!users.length) {
            throw new Error('User not found!')
        }

        const user = users[0];

        this._checkRevokedToken(user);
        
        return this._userWoDPP(user);
    }

    private _userWoDPP(user: User): User {
        delete user.token_revoked;

        return user;
    }

    private _checkRevokedToken(user: User): void {
        if (typeof user.token_revoked === 'number' && user.token_revoked === 1) {
            throw new UserTokenRevokedError('User token has been revoked');
        }
    }

}
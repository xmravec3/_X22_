import { User, UserType } from '../domains/User';
import IPasswordValidator from '../../../security/interfaces/IPassword';

export default interface IUserCatalog {

    getByID(id: number, userType: UserType): Promise<User>
    getByLogin(login: string, userType: UserType): Promise<User>
    getByCredentials(login: string, passwordValidator: IPasswordValidator, userType: UserType): Promise<User>
    getByToken(id: number, token: string): Promise<User>;
    saveToken(id: number, token: string): Promise<void>;
    deleteToken(id: number, token: string): Promise<void>;
    deleteAllTokens(id: number): Promise<void>;

}
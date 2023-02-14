import 'dotenv/config';
import IJWToken from './interfaces/IJWToken';
import { sign, verify } from 'jsonwebtoken';
import { UserType } from '../catalogs/common/domains/User';

export default class JWToken implements IJWToken {

    private token: string;

    constructor(token: string) {
        this.token = token;
    }

    static generateToken(identifier: number, login: string, name: string, email :string, userType: UserType): string {
        return sign({ id: identifier, login, name, email, userType }, String(process.env.JWT_SECRET), process.env.JWT_EXPIRES_IN_SECONDS ? { expiresIn: `${process.env.JWT_EXPIRES_IN_SECONDS}s` } : undefined);
    }

    verify(): { id: number, userType: UserType } {
        const { id, userType } = verify(this.token, String(process.env.JWT_SECRET)) as {id: number, userType: UserType};

        return { id, userType };
    }

}
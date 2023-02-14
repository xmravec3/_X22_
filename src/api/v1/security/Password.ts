import IPassword from './interfaces/IPassword';
import { compare, hash } from 'bcryptjs';

export default class Password implements IPassword {
    private password: string;

    constructor(password: string) {
        this.password = password;
    }

    async validate(password: string): Promise<boolean> {
        return compare(this.password, password);
    }

    async hashPassword(): Promise<string> {
        return hash(this.password, 8);
    }

}
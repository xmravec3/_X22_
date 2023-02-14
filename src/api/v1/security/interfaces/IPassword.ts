export default interface IPassword {

    validate(password: string): Promise<boolean>;
    hashPassword(): Promise<string>;

}
export default interface IJWToken {

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    verify(token: string): any;

}
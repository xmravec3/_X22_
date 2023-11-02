export default interface IMessageBroker {
    get(key: string): Promise<string|null>;
    set(key: string, value: string): Promise<void>;
    expire(key: string, seconds: number): Promise<void>;
}
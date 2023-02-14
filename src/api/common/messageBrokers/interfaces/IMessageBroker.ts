export default interface IMessageBroker {
    closeConnection(): Promise<void>;
    sendToQueue(queue: string, content: unknown, options?: object | undefined): Promise<boolean>;
}
import amqplib, { Channel, Connection } from 'amqplib'
import IMessageBroker from '../interfaces/IMessageBroker';

export default class RabbitMQBroker implements IMessageBroker {

    private _server: string;
    private _connection: Connection | undefined = undefined;
    private _channel: Channel | undefined = undefined;

    constructor(host: string, user: string, password: string) {
        this._server = this._buildServerString(host, user, password);
    }

    async sendToQueue(queue: string, content: string, options?: object | undefined): Promise<boolean> {
        const channel = await this._getChannel(this._server);

        await channel.assertQueue(queue, {
            durable: true
        });

        return channel.sendToQueue(queue, Buffer.from(content), options)
    }

    async closeConnection(): Promise<void> {
        if (this._channel) {
            this._channel.close();
        }
        
        if (this._connection) {
            this._connection.close();
        }
    }

    private async _getChannel(server: string): Promise<Channel> {
        if (!this._channel) {
            this._connection = await amqplib.connect(server);
            this._channel = await this._connection.createChannel();
        }

        return this._channel;
    }

    private _buildServerString(host: string, user: string, password: string): string {
        return `amqp://${ user }:${ password }@${ host }`;
    }

}
import 'dotenv/config';
import IMessageBroker from './interfaces/IMessageBroker';
import RabbitMQBroker from './engines/RabbitMQBroker';

export const MessageBrokerEngine = {
    RabbitMQ: RabbitMQBroker
}

export enum MessageBrokerType {
    RabbitMQ = 'RabbitMQ'
}

type AvailableMassgeBroker = {
    engine: string,
    host: string,
    user: string,
    password: string,
    instance: IMessageBroker
}

export default class MessageBroker {

    private static availableBrokers: AvailableMassgeBroker[] = [];

    public static get(): IMessageBroker {
        const { MESSAGE_BROKER_ENGINE, MESSAGE_BROKER_HOST, MESSAGE_BROKER_USER, MESSAGE_BROKER_PASSWORD } = process.env;

        const engineKey = String(MESSAGE_BROKER_ENGINE);
        const host = String(MESSAGE_BROKER_HOST);
        const user = String(MESSAGE_BROKER_USER);
        const password = String(MESSAGE_BROKER_PASSWORD);

        const broker = MessageBroker.findAvailableBroker(engineKey, host, user, password);

        if (broker) {
            return broker.instance;
        }

        const engine = MessageBrokerEngine[engineKey as keyof typeof MessageBrokerEngine];

        if (!engine) {
            throw new Error(`Message Broker '${engineKey}' does not exist`);
        }

        const instance = new engine(host, user, password);

        MessageBroker.availableBrokers.push({
            engine: engineKey,
            host: host,
            user: user,
            password: password,
            instance
        });

        return instance;
    }

    private static findAvailableBroker(engine: string, host: string, user: string, password: string): AvailableMassgeBroker | undefined {
        return MessageBroker.availableBrokers.find(broker => {
            return broker.engine === engine &&
                broker.host === host &&
                broker.user === user &&
                broker.password === password;
        });
    }

}
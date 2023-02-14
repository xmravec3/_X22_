import 'dotenv/config';
import IConnector from './interfaces/IConnector';
import MySQLConnector from './engines/MySQLConnector';

export const ConnectorEngine = {
    MYSQL: MySQLConnector
}

export enum ConnectorType {
    MYSQL = 'MYSQL'
}

type AvailableConnector = {
    engine: string,
    host: string,
    user: string,
    database: string,
    instance: IConnector
}

export default class Connector {

    private static availableConnectors: AvailableConnector[] = [];

    static get(): IConnector {
        const { DB_ENGINE, DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE } = process.env;

        const engineKey = String(DB_ENGINE);
        const host = String(DB_HOST);
        const user = String(DB_USER);
        const password = String(DB_PASSWD);
        const database = DB_DATABASE || '';

        const connector = Connector.findAvailableConnector(engineKey, host, user, database);

        if (connector) {
            return connector.instance;
        }

        const engine = ConnectorEngine[engineKey as keyof typeof ConnectorEngine];

        if (!engine) {
            throw new Error(`Connector '${engineKey}' does not exist`);
        }

        const instance = new engine(host, user, password, database);

        Connector.availableConnectors.push({
            engine: engineKey,
            host: host,
            user: user,
            database: database,
            instance
        });

        return instance;
    }

    private static findAvailableConnector(engine: string, host: string, user: string, database: string): AvailableConnector | undefined {
        return Connector.availableConnectors.find(connector => {
            return connector.engine === engine &&
                connector.host === host &&
                connector.user === user &&
                connector.database === database;
        });
    }
}
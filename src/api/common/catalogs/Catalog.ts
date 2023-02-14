import Connector from '../connectors/Connector';
import IConnector from '../connectors/interfaces/IConnector';

export default abstract class Catalog {

    static connector: IConnector;

    static getConnector(): IConnector {
        if (!this.connector) {
            this.connector = Connector.get();
        }

        return this.connector;
    }

}
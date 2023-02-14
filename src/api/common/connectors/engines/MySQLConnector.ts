import { Connection, createConnection, escape } from 'mysql';
import IConnector, { Query, TransactionQuery } from '../interfaces/IConnector';

export default class MySQLConnector implements IConnector {
    private host: string;
    private user: string;
    private password: string;
    private database: string | undefined;

    constructor(host: string, user: string, password: string, database: string | undefined = undefined) {
        this.host = host;
        this.user = user;
        this.password = password;
        this.database = database;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async query({ query, bindings = [] }: Query): Promise<any> {
        const connection = this._openConnection();

        try {
            return await this._buildQueryPromise(connection, query, bindings);
        } finally {
            this._closeConnection(connection);
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async transaction(queries: TransactionQuery[]): Promise<any[]> {
        if (!queries.length) {
            throw new Error('No query is provided');
        }

        const connection = this._openConnection();

        try {
            return await new Promise((resolve, reject) => {
                connection.beginTransaction(async error => {
                    if (error) {
                        return reject(error);
                    }

                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    const results: any[] = [];

                    try {
                        for (const { query, bindings = [], deriveBindingsCallback } of queries) { // NEVER use array.forEach with async => does not handle thown exceptions
                            const derivedBindings = deriveBindingsCallback ? await deriveBindingsCallback(results, bindings) : bindings;

                            results.push(await this._buildQueryPromise(connection, query, derivedBindings));
                        }

                        await new Promise((resolve, reject) => {
                            connection.commit(error => {
                                if (error) {
                                    return reject(error);
                                }

                                resolve(null);
                            });
                        })
                    } catch (error) {
                        return reject(error);
                    }

                    resolve(results);
                })
            })
        } catch (error) {
            connection.rollback();

            throw error;
        } finally {
            this._closeConnection(connection);
        }
    }

    escape(value: unknown) {
        return escape(value);
    }

    private _openConnection(): Connection {
        const connection = createConnection({
            host: this.host,
            user: this.user,
            password: this.password,
            database: this.database,
            insecureAuth: true
        });

        connection.connect();

        return connection;
    }

    private _closeConnection(connection: Connection): void {
        connection.end();
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _buildQueryPromise(connection: Connection, query: string, bindings: string[]): Promise<any> {
        return new Promise((resolve, reject) => {
            connection.query(query, bindings, (error, results) => {
                if (error) {
                    return reject(error);
                }

                resolve(results);
            });
        });
    }
}
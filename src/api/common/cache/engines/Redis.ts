import { RedisClientType, createClient } from 'redis';
import ICache from '../interfaces/ICache';

export default class Redis implements ICache {

    private _host: string;
    private _user: string;
    private _password: string;
    private _client: RedisClientType | undefined;

    constructor(host: string, user: string, password: string) {
        this._host = host;
        this._user = user;
        this._password = password;
    }

    async get(key: string): Promise<string|null> {
        const client = await this._getClient(this._host, this._user, this._password);

        return await client.get(key);
    }

    async set(key: string, value: string): Promise<void> {
        const client = await this._getClient(this._host, this._user, this._password);

        await client.set(key, value);
    }

    async expire(key: string, seconds = 0): Promise<void> {
        const client = await this._getClient(this._host, this._user, this._password);

        await client.expire(key, seconds);
    }

    private async _getClient(host: string, user: string, password: string): Promise<RedisClientType> {
        if (!this._client || !this._client.isOpen || !this._client.isReady) {
            this._client = createClient({
                username: user,
                password: password,
                socket: {
                    host: host,
                    port: 6379,
                    tls: false
                }
            })

            this._client.on('error', (error) => console.error(`Error : ${error}`));

            await this._client.connect();
        }

        return this._client;
    }

}
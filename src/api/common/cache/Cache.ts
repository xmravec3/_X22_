import 'dotenv/config';
import ICache from './interfaces/ICache';
import Redis from './engines/Redis';

export const CacheEngine = {
    Redis: Redis
}

export enum MessageBrokerType {
    Redis = 'Redis'
}

type AvailableCacheInstances = {
    engine: string,
    host: string,
    user: string,
    password: string,
    instance: ICache
}

export default class Cache {

    private static availableInstances: AvailableCacheInstances[] = [];

    public static get(): ICache {
        const { CACHE_ENGINE, CACHE_HOST, CACHE_USER, CACHE_PASSWD } = process.env;

        const engineKey = String(CACHE_ENGINE);
        const host = String(CACHE_HOST);
        const user = String(CACHE_USER);
        const password = String(CACHE_PASSWD);

        const broker = Cache.findAvailableInstance(engineKey, host, user, password);

        if (broker) {
            return broker.instance;
        }

        const engine = CacheEngine[engineKey as keyof typeof CacheEngine];

        if (!engine) {
            throw new Error(`Cache engine '${engineKey}' does not exist`);
        }

        const instance = new engine(host, user, password);

        Cache.availableInstances.push({
            engine: engineKey,
            host: host,
            user: user,
            password: password,
            instance
        });

        return instance;
    }

    private static findAvailableInstance(engine: string, host: string, user: string, password: string): AvailableCacheInstances | undefined {
        return Cache.availableInstances.find(cache => {
            return cache.engine === engine &&
                cache.host === host &&
                cache.user === user &&
                cache.password === password;
        });
    }

}
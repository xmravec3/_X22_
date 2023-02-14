/* eslint-disable @typescript-eslint/no-explicit-any */
export type Query = {
    query: string,
    bindings?: any[]
}

export type TransactionQuery = Query & {
    deriveBindingsCallback?: (results: any[], actualBindings?: any[]) => Promise<any[]>
}

export default interface IConnector {

    query(query: Query): Promise<any>;

    transaction(queries: TransactionQuery[]): Promise<any[]>;

    escape(value: any): any;
}
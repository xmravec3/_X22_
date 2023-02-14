export enum UserType {
    Editor = 1
}

export enum EditorPermission {
    Users = 'users',
    Content = 'content'
}

export type User = {
    id: number,
    login: string,
    password?: string,
    name: string,
    email: string,
    permissions?: {
        content: boolean,
        users: boolean
    } | null,
    token?: string,
    token_revoked?: number
};
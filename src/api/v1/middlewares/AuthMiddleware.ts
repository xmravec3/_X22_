import UserCatalog from '../catalogs/common/UserCatalog';
import JWToken from '../security/JWToken';
import { Request, Response, NextFunction } from 'express';
import { UserType } from '../catalogs/common/domains/User';
import UserTokenRevokedError from '../catalogs/common/exceptions/UserTokenRevokedError';
import UserNotPermittedError from './exceptions/UserNotPermittedError';

export default (userType: UserType, authenticationRequired = true) => async (request: Request, response: Response, next: NextFunction) => {
    try {
        const bearerToken = request.header('Authorization');
        if (!bearerToken) {
            if (authenticationRequired) {
                throw new Error('Authorization header not received');
            } else {
                return next();
            }
        }

        const token = String(bearerToken.replace('Bearer ', ''));
        const { id: userID, userType: userTypeFromToken } = new JWToken(token).verify();

        if (userType !== userTypeFromToken) {
            throw new Error('User type not matched');
        }

        const user = await new UserCatalog().getByToken(userID, token);

        Object(request).token = token;
        Object(request).user = user; // save the user to use it later in routes
        next();
    } catch (error) {
        if (error instanceof UserTokenRevokedError) {
            return response.status(403).send({
                error: {
                    name: 'JWT__Revoked',
                    message: error.message
                }
            })
        } else if (error instanceof UserNotPermittedError) {
            return response.status(403).send({
                error: {
                    name: 'JWT_UserNotPermitted',
                    message: error.message
                }
            })
        }

        response.status(401).send({ error: 'Please authenticate' })
    }
}
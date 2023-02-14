import UserCatalog from '../../catalogs/common/UserCatalog';
import { Router as expressRouter } from 'express';
import Password from '../../security/Password';
import JWToken from '../../security/JWToken';
import authMiddleware from '../../middlewares/AuthMiddleware';
import { User, UserType } from '../../catalogs/common/domains/User';

export default (userType: UserType = UserType.Editor) => {
    const router = expressRouter();
    const userCatalog = new UserCatalog();

    router.post('/login', async (request, response) => {
        try {
            const user = await userCatalog.getByCredentials(request.body.login, new Password(request.body.password), userType);

            const token = JWToken.generateToken(user.id, user.login, user.name, user.email, userType);

            await userCatalog.saveToken(user.id, token);

            response.send({
                user,
                token
            });
        } catch (error) {
            response.status(401).send({ error: 'Please authenticate' });
        }
    });

    router.post('/logout', authMiddleware(userType), async (request, response) => {
        try {
            await userCatalog.deleteToken((<User>Object(request).user).id, Object(request).token);

            response.send()
        } catch (error) {
            response.status(500).send()
        }
    });

    router.post('/logout/all', authMiddleware(userType), async (request, response) => {
        try {
            await userCatalog.deleteAllTokens((<User>Object(request).user).id);

            response.send()
        } catch (error) {
            response.status(500).send()
        }
    });

    router.get('/me', authMiddleware(userType), async (request, response) => {
        try {
            const user = await userCatalog.getByID((<User>Object(request).user).id, userType);

            response.send({
                ...user
            });
        } catch (error) {
            response.status(401).send({ error: 'Please authenticate' });
        }
    });

    return router;
};
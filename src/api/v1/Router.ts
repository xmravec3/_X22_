import { Router as expressRouter } from 'express';

import userRouter from './routers/common/UserRouter';

export default () => {
    const router = expressRouter();

    // student
    router.use(userRouter());

    return router;
};
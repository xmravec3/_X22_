import { Router as expressRouter } from 'express';

import userRouter from './routers/common/UserRouter';
import videoRouter from './routers/VideoRouter';
import climberRouter from './routers/ClimberRouter';
import knnRouter from './routers/KNNRouter';
import chartDataRouter from './routers/ChartDataRouter';
import helloRouter from './routers/HelloRouter';

export default () => {
    const router = expressRouter();

    router.use(videoRouter());
    router.use(userRouter());
    router.use(climberRouter());
    router.use(knnRouter());
    router.use(chartDataRouter());
    router.use(helloRouter());


    return router;
};
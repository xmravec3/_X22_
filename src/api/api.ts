import express, { json as expressJson } from 'express';
import cors from 'cors';

import router_v1 from './v1/Router';

export default () => {
    const app = express();

    app.use(expressJson({limit: '10mb'}));
    app.use(cors());

    const v1 = router_v1();

    app.use('/v1', v1);
    app.use('/latest', v1);

    return app;
};
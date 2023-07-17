import VideoCatalog from '../catalogs/VideoCatalog';
import { Router as expressRouter } from 'express';

export default () => {
    const router = expressRouter();
    const videoCatalog = new VideoCatalog();

    router.get('/videoInfo/:id', async (request, response) => {
        try {
            response.send( await videoCatalog.getByIDVideoInfo( +request.params.id ));
        } catch (error) {
            response.status(500).send({ error: 'Unknow video' });
        }
    });

    router.get('/videos/:id', async (request, response) => {
        try {
            response.send( await videoCatalog.getByID( +request.params.id ));
        } catch (error) {
            response.status(500).send({ error: 'Unknow video' });
        }
    });

    router.get('/videos', async (request, response) => {
        try {
            response.send( await videoCatalog.getAll());
        } catch (error) {
            response.status(500).send({ error: 'Unknow videos' });
        }
    });

    router.get('/videosBasic', async (request, response) => {
        try {
            response.send( await videoCatalog.getAllBasic());
        } catch (error) {
            response.status(500).send({ error: 'Unknow videos' });
        }
    });

    router.get('/datesAll', async (request, response) => {
        try {
            response.send( await videoCatalog.getAllDates());
        } catch (error) {
            response.status(500).send({ error: 'Unknow issue with dates' });
        }
    });

    return router;
};
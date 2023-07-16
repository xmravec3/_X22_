import ClimberCatalog from '../catalogs/ClimberCatalog';
import { Router as expressRouter } from 'express';

export default () => {
    const router = expressRouter();
    const climberCatalog = new ClimberCatalog();

    router.get('/climbers/:id', async (request, response) => {
        try {
            response.send( await climberCatalog.getByID( +request.params.id ));
        } catch (error) {
            response.status(500).send({ error: 'Unknow climber' });
        }
    });

    router.get('/climbers', async (request, response) => {
        try {
            response.send( await climberCatalog.getAll());
        } catch (error) {
            response.status(500).send({ error: 'Unknow climbers' });
        }
    });

    router.get('/climbersAll', async (request, response) => {
        try {
            response.send( await climberCatalog.getAllWithVideo());
        } catch (error) {
            response.status(500).send({ error: 'Unknow climbers' });
        }
    });

    return router;
};
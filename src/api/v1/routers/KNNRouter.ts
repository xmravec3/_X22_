import { Router as expressRouter } from 'express';
import { spawn } from 'child_process';
import path from 'path';
import 'dotenv/config';
import Cache from '../../common/cache/Cache';
//import { cwd } from 'node:process';

export default () => {
    const router = expressRouter();

    router.get('/knn/:id', async (request, response) => {

        const id = request.params.id;

        const cacheKey = `knn-${id}`;

        try {
            const jsonString = await Cache.get().get(cacheKey);

            if (jsonString) {
                return response.send(JSON.parse(jsonString));
            }

            console.log('Current CWD is:')
            const pythonScriptPath = path.join(process.cwd(), 'getKNNForDB.py');
            console.log(pythonScriptPath)
            
            const pythonCommand = String(process.env.PYTHON_COMMAND);
            console.log('Python command path: ', pythonCommand);

            //console.log(`Current directory: ${cwd()}`);
            const python = spawn(pythonCommand, [pythonScriptPath, id], { shell: true });
            const result: any[] = [];
            //let result = [];

            // collect data from script
            python.stdout.on('data', function (data) {
                console.log('Pipe data from python script ...');
                result.push(data);
            })

            // in close event we are sure that stream is from child process is closed
            python.on('close', async (code) => {
                console.log(`child process close all stdio with code ${code}`)
                if (code !== 0) {
                    console.error(`Python script exited with code ${code}`);
                    response.status(500).send({ error: 'Python issue' }); // added
                return;
            }
  
            const jsonResult = Buffer.concat(result).toString();

            await Cache.get().set(cacheKey, jsonResult);

            const parsedResult = JSON.parse(jsonResult);
  
            response.send(parsedResult);
        })
        } catch (error) {
            response.status(500).send({ error: 'Unknow id of video' });
        }
    });


    return router;
};
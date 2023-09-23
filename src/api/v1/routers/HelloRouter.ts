import { Router as expressRouter } from 'express';
import { spawn } from 'child_process';
import path from 'path';
import 'dotenv/config';
//import { cwd } from 'node:process';

export default () => {
    const router = expressRouter();

    router.get('/hello', async (request, response) => {

        try {
            //console.log(`Current directory: ${cwd()}`);
            //const scriptFilename = path.join(__dirname, 'pythonTest', 'main.py');
            console.log('Current CWD is:')
            const pythonScriptPath = path.join(process.cwd(), 'pythonTest', 'main.py');
            console.log(pythonScriptPath)

            const pythonCommand = String(process.env.PYTHON_COMMAND);
            console.log('Python command path: ', pythonCommand);
            
            console.log('*********************************')
            const python = spawn(pythonCommand, [pythonScriptPath], { shell: true });
            const result: any[] = [];
            //let result = [];

            // collect data from script
            python.stdout.on('data', function (data) {
                console.log('Pipe data from python script ...');
                result.push(data);
            });

            // in close event we are sure that stream is from child process is closed
            python.on('close', (code) => {
                console.log(`child process close all stdio with code ${code}`)
                if (code !== 0) {
                    console.error(`Python script exited with code ${code}`);
                    response.status(500).send({ error: 'Python issue' }); // added
                    return;
                }
  
            const jsonResult = Buffer.concat(result).toString();
            const parsedResult = JSON.parse(jsonResult);
  
            response.send(parsedResult);
        })
        } catch (error) {
            response.status(500).send({ error: 'Unknow id of video' });
        }
    });


    return router;
};
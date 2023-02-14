import app from './api';
import MessageBroker from './common/messageBrokers/MessageBroker';
const port = process.env.PORT || 3000;

const api = app();

const server = api.listen(port, () => {
    console.log('Server is up on port ' + port);
});

['exit', 'SIGINT', 'SIGTERM'].forEach((eventType) => {
    process.on(eventType, async () => {
        console.log('shutdown', eventType);

        server.close();
        await MessageBroker.get().closeConnection();

        process.exit();
    })
})
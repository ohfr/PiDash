import { io } from 'socket.io-client';

// this will only ever run locally
const url = 'http://0.0.0.0:5000';

export const socket = io(url);
import { io } from 'socket.io-client';

// this will only ever run locally
const url = 'http://192.168.1.41:5000';

export const socket = io(url);
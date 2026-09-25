import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const chatWithAgent = async (message) => {
    const response = await axios.post(`${API_URL}/chat`, { message }, { timeout: 60000 });
    return response.data;
};

export const clearChat = async () => {
    const response = await axios.post(`${API_URL}/chat/clear`);
    return response.data;
};

export const fetchMenu = async () => {
    const response = await axios.get(`${API_URL}/menu`);
    return response.data;
};

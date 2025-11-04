import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

export const getAllTransportServices = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/services-transport`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getCamionsDechets = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/camions-dechets`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getTransportsDangereux = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/transports-dechets-dangereux`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const addTransportService = async (serviceData) => {
    try {
        const response = await axios.post(`${BASE_URL}/services-transport`, serviceData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateTransportService = async (id, serviceData) => {
    try {
        const response = await axios.put(`${BASE_URL}/services-transport/${id}`, serviceData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteTransportService = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/services-transport/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Camions Déchets ==========
export const createCamionDechets = async (camionData) => {
    try {
        const response = await axios.post(`${BASE_URL}/camions-dechets`, camionData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getCamionDechets = async (id) => {
    try {
        const response = await axios.get(`${BASE_URL}/camions-dechets/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateCamionDechets = async (id, camionData) => {
    try {
        const response = await axios.put(`${BASE_URL}/camions-dechets/${id}`, camionData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteCamionDechets = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/camions-dechets/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Transport Déchets Dangereux ==========
export const createTransportDangereux = async (transportData) => {
    try {
        const response = await axios.post(`${BASE_URL}/transports-dechets-dangereux`, transportData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getTransportDangereux = async (id) => {
    try {
        const response = await axios.get(`${BASE_URL}/transports-dechets-dangereux/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateTransportDangereux = async (id, transportData) => {
    try {
        const response = await axios.put(`${BASE_URL}/transports-dechets-dangereux/${id}`, transportData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteTransportDangereux = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/transports-dechets-dangereux/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};
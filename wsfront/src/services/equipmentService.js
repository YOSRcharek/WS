import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

export const getAllEquipments = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/equipements`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getBroyeurs = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/broyeurs`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getCamionsBenne = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/camions-benne`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getCompacteurs = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/compacteurs`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getConteneurs = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/conteneurs`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const addEquipment = async (equipmentData) => {
    try {
        const response = await axios.post(`${BASE_URL}/equipements`, equipmentData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateEquipment = async (id, equipmentData) => {
    try {
        const response = await axios.put(`${BASE_URL}/equipements/${id}`, equipmentData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteEquipment = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/equipements/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Broyeurs ==========
export const createBroyeur = async (broyeurData) => {
    try {
        const response = await axios.post(`${BASE_URL}/broyeurs`, broyeurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateBroyeur = async (id, broyeurData) => {
    try {
        const response = await axios.put(`${BASE_URL}/broyeurs/${id}`, broyeurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteBroyeur = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/broyeurs/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Camions Benne ==========
export const createCamionBenne = async (camionData) => {
    try {
        const response = await axios.post(`${BASE_URL}/camions-benne`, camionData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateCamionBenne = async (id, camionData) => {
    try {
        const response = await axios.put(`${BASE_URL}/camions-benne/${id}`, camionData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteCamionBenne = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/camions-benne/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Compacteurs ==========
export const createCompacteur = async (compacteurData) => {
    try {
        const response = await axios.post(`${BASE_URL}/compacteurs`, compacteurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateCompacteur = async (id, compacteurData) => {
    try {
        const response = await axios.put(`${BASE_URL}/compacteurs/${id}`, compacteurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteCompacteur = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/compacteurs/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// ========== CRUD pour Conteneurs ==========
export const createConteneur = async (conteneurData) => {
    try {
        const response = await axios.post(`${BASE_URL}/conteneurs`, conteneurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateConteneur = async (id, conteneurData) => {
    try {
        const response = await axios.put(`${BASE_URL}/conteneurs/${id}`, conteneurData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteConteneur = async (id) => {
    try {
        const response = await axios.delete(`${BASE_URL}/conteneurs/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};